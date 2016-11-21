import grako
import json
import clparser
import clparsersemantics
import pexpect

class codeGenerator(): 
	def __init__(self, fileName):
		self.sourceFile = fileName
		self.sourceText = (open(self.sourceFile, "r").readlines())
		self.printSourceText = True 
		self.preprocessing()

		self.parser = clparser.UnknownParser(parseinfo=True)
		self.parseTree = self.parser.parse(self.sourceText, rule_name='program', semantics=clparsersemantics.UnknownSemantics())
		self.printTree = True 
		self.printParseTree()
		
		self.test_types_to_declare = []

		self.availableFunctions = ["print"]
		self.loadedFunctions = []
		##	When loading in functions from std lib check for availability and for load status.
		##	The _start section will contain the code the is needed when the funciton is to be called,
		## 	the rest of the labels and data reservations should be copied exactly into the source file.
		##	Be careful when reading/copying sections from stdLib because the order of the labels may be 
		## 	important (within each function's source template). Therefore it should always be assumed that it is. 


		self.xSourceFile = "x86_tests/clTest.asm"
		self.xData = ["section .data\n"]
		self.xBss = ["section .bss\n"]
		self.xText = ["\nsection .text\n", "\tglobal _start\n"]
		self.xStart = ["\n_start:\n"]

		self.functionCode = ["_exit:\n\tmov rax, 60\n\tmov rdi, 0\n\tsyscall\n"]
		self.functionTriggers = {} #dict {funcname => list of trigger lines}
		

		self.blockId = ["g"]
		self.blockCount = 1
		

	def preprocessing(self):
                temp = []
                skip = False
                for i, line in enumerate(self.sourceText):
                        if skip:
                                skip = False
                                continue
                        if "&" in line:
                                tempStr = line.replace("&", self.sourceText[i+1].replace("\n", ""))
                                skip = True
                                temp.append(tempStr)
                        else:
				if line != "" and line != "\n":
                                	temp.append(line)
                
			processedText = ""
                for x in temp:
                        processedText += x

                processedText = "@@@" + processedText + "@@@"       # using "@@@" to denote start and end of file makes
                							# some parseing tasks easier 
		if self.printSourceText: 
			print("\n================== " + self.sourceFile + " ==================")
			print repr(processedText) + "\n"
			
		self.sourceText = str(processedText)

	def printParseTree(self): 
		if self.printTree: 
			print("\n================== Syntax Tree ==================")
                	print(json.dumps(self.parseTree, indent=2)) # ASTs are JSON-friendy
			print("==================================================")

	
	def traverseParseTree(self, parseTree):
		
		print "\n" + str(type(parseTree)) + ":" + str(parseTree) + "\n"

		if type(parseTree) == dict:
			if not parseTree:
				return 

			if parseTree["type"] == "program":
				for item in parseTree["value"]:
					self.traverseParseTree(item)	
			
			if parseTree["type"] == "type_declaration": 
				self.declare_type(parseTree)
			
			if parseTree["type"] == "block":
				self.blockId.append(self.genBlockId())
				for item in parseTree["value"]:
					self.traverseParseTree(item)

			if parseTree["type"] == "function_call":###########################################################
				print("PLACEHOLDER FOR FUNCTION CALL HANDLING")
				self.call_function(parseTree["value"])

		elif type(parseTree) == grako.contexts.Closure:
			for x in parseTree:
				self.traverseParseTree(x)		
	
		# return on unhandled object
		return 	
	
	def declare_type(self, parseTree):
		if parseTree["type"] == "type_declaration": 
			
			myType = ""
			myName = ""
			myLiteral = ""

			decTree = parseTree["value"]
			for token in decTree:
				if type(token) == dict:
					if token["type"] == "type_keyword":
						myType = token["value"]
					
					if token["type"] == "var_name":
						myName = token["value"]
					
					if token["type"] == "value":
						myLiteral = token["value"]["value"]

			myLiteral = self.clean_literal(myLiteral, myType)			

			##
			##	ASSEMBLY VARIABLE FORMAT
			##	<scope id>_<type>_<name>
			##	<scope id>_<value>_<name>


			if myType == "int":
				myName_val = self.blockId[-1] + "_val_" + myName 
				myName_type = self.blockId[-1] + "_type_" + myName
				
				self.xBss.append("\t" + myName_val + ":\t resq 1\n")
				self.xBss.append("\t" + myName_type + ":\t resb 1\n")

				self.xStart.append("\tmov word [" + myName_val + "], " + myLiteral + "\n")
				self.xStart.append("\tmov byte [" + myName_type + '], "i"\n')
			
			if myType == "char":
				myName_val = self.blockId[-1] + "_val_" + myName 
				myName_type = self.blockId[-1] + "_type_" + myName

				self.xBss.append("\t" + myName_val + ":\t resb 1" "\n")
				self.xBss.append("\t" + myName_type + ":\t resb 1" "\n")
				
				self.xStart.append("\tmov byte [" + myName_val + "], " + myLiteral + "\n")	
				self.xStart.append("\tmov byte [" + myName_type + '], "c"\n')

		else: 
			print("!!! -- ERROR -- !!! - declare_type")
			return 
	

	def clean_literal(self, tree, myType):
		if myType == "int":
			return tree
		if myType == "char":
			return tree[0] + tree[1] + tree[2]

	def call_function(self, tree):
		# will only work with single arg right now, additional infrastructure will be needed to handle multiple args 
		fName = tree[0]["value"]
		argName = tree[2]["value"]["value"]

		print(fName, argName)

		if fName in self.availableFunctions:
			if fName not in self.loadedFunctions:
				self.load_function_from_lib(fName)
				self.loadedFunctions.append(fName)

			if fName in self.loadedFunctions:
				myTrigger = str(self.functionTriggers[fName])
				myTrigger = myTrigger.replace("<INSERT_VALUE>", self.blockId[-1] + "_val_" + argName)
				myTrigger = myTrigger.replace("<INSERT_TYPE>", self.blockId[-1] + "_type_" + argName)
				myTrigger = myTrigger.split("\n")
				for line in myTrigger:
					print line
					self.xStart.append(line + "\n")

		else:
			raise "ATTEMPING TO CALL A NON EXISTANT FUNCTION"

	def write_x86_source(self):
		with open(self.xSourceFile, "w+") as s:
			if len(self.xData) > 1:
				for x in self.xData:
					s.write(str(x))	

			if len(self.xBss) > 1:
				for x in self.xBss:
					s.write(str(x))

			for x in self.xText:
                            	s.write(str(x))	


			for x in self.xStart:
				s.write(str(x))
			

			for section in self.functionCode:
				s.write(section)


	def genBlockId(self):
		temp = self.blockCount
		effectiveAlphabet = ["a", "b", "c", "d", "e", "f", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
		idStr = ""

		# using len in case other letters need to me removed becase they are reserved, g is removed
		# because it is the label for the global scope 

		if temp / len(effectiveAlphabet) > 0:
			idStr.append(effectiveAlphabet[temp / len(effectiveAlphabet)])
			temp = temp % len(effectiveAlphbet)

		idStr.append(effectiveAlphabet[temp])
		self.blockCount+=1
		return temp


	def load_function_from_lib(self, fName):
		try:
			with open("standardLib/" + fName + ".asm") as f:
				primaryFlag = False
				primaryCode = []
				index = 0
				func = f.readlines()
				for i, line in enumerate(func):
					if "section .bss" in line:
						bssTemp = []
						for x in range((i+1), len(func)):
							if "section" in func[x]: break
							else: bssTemp.append(func[x])

					if "section .text" in line:
						continue ## should be fine, nothing should be in .text
				
					if "_start:" in line:
						startTemp = ""
						for x in range((i+1), len(func)):
                                                	if "_" in func[x] and ":" in func[x]:
								primaryFlag = True 
								index = x-1
								break  ## catch new section 
                                                	else: startTemp += func[x]
				
					if primaryFlag and i > index:
						primaryCode.append(line)

			#print ("bss: " + str(bssTemp))
			self.xBss.extend(bssTemp)	
			#print ("start: " + str(startTemp))
			self.functionTriggers[fName] = startTemp
			print ("code: ")
			for x in primaryCode: print(x)
			self.functionCode.extend(primaryCode)

		except Exception as e:
			print(" === ERROR READING LIBRARY FINCTION ===")
			print(e)
			return 

		# Need to strip empty lines at the end of this function 

	def assemble(self, outfile):
		#self.xSourceFile 
		p = pexpect.spawn("bash")
		p.expect(":~") ## expect most recent prompt 
		p.sendline("cd x86_tests")
		p.expect(":~")
		p.sendline("nasm -f elf64 -o test.o " + outfile + ".asm") #assemble code 
		p.expect(":~")
		p.sendline("ld test.o -o " + outfile)
		x = p.expect(":~")
		y = p.before
		print x 
		print y


























