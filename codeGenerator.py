import grako
import json
import clparser
import clparsersemantics 

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
		self.xSourceFile = "x86_tests/clTest.asm"
		self.xData = ["section .data\n"]
		self.xBss = ["section .bss\n"]
		self.xText = ["\nsection .text\n", "\tglobal _start\n"]
		self.xStart = ["\n_start:\n"]

		
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
			print processedText + "\n"
			
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
			
			# load and execute 'sys_exit'
			s.write("\tmov rax, 60\n")
			s.write("\tmov rdi, 0\n")
			s.write("\tsyscall\n")



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

































