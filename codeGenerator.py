import grako
import json
import clparser
import clparsersemantics
import pexpect
import sys 

class codeGenerator(): 
	def __init__(self, fileName):
		self.sourceFile = fileName
		self.sourceText = (open(self.sourceFile, "r").readlines())
		self.printSourceText = True 
		self.preprocessing()

		self.parser = clparser.UnknownParser(parseinfo=True, whitespace='')
		self.parseTree = self.parser.parse(self.sourceText, rule_name='program', semantics=clparsersemantics.UnknownSemantics())
		self.printTree = True 
		self.printParseTree()
		
		self.test_types_to_declare = []

		self.availableFunctions = ["print", "cl_bool_op"]
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
		
		self.variables = {"g":{} } # NEW FORMAT scope: {name: type}                                              #varName: x, info: {scope, value?, type}
		self.xBss.append("\texprResolutionBuffer:   resq 1\n")
		self.xBss.append("\tindexBuffer:	resq 1\n")

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
		if type(parseTree) == dict:
			if not parseTree:
				return 

			if parseTree["type"] == "program":
				for item in parseTree["value"]:
					self.traverseParseTree(item)	
			
			if parseTree["type"] == "type_declaration": 
				self.declare_type(parseTree)
			
			if parseTree["type"] == "block":
				self.blockId.append(self.genBlockId()) # push block identifier onto stack 
				self.variables[self.blockId[-1]] = {}  # grab last identifier and carve out a place for this blocks vars 
				self.blockCount+=1
				self.xStart.append("_" + self.blockId[-1] + "_block_header:\n")
				for item in parseTree["value"]:
					self.traverseParseTree(item)
				self.xStart.append("_" + self.blockId[-1] + "_block_footer:\n")
				self.blockId.pop()

			if parseTree["type"] == "function_call":
				self.call_function(parseTree["value"])

			if parseTree["type"] == "assignment":
				self.assign_value(parseTree["value"])
			
			if parseTree["type"] == "condition_statement":
				self.condition_statement_handler(parseTree["value"])
			
			if parseTree["type"] == "loop_statement":
				self.loop_statement_handler(parseTree["value"])


		elif type(parseTree) == grako.contexts.Closure:
			for x in parseTree:
				self.traverseParseTree(x)		
	
		# return on unhandled object
		return 	
	
	def scope_resolver(self, var_name):
		print("===== Scope Resolution ====")##############################################################################
		myBlock = self.blockId[-1]
		print "\tmy block: ", myBlock
		blockStack = list(self.blockId)
		blockStack.reverse()
		print blockStack
		
		for bId in blockStack:						# self.variables everwhere/
			if var_name in self.variables[bId]:
				print("found variable: " + var_name + " in: " + bId)
				print("==== Scope Resolution end ====\n\n")###################################### 
				return bId

		print("ERROR: " + var_name + " out of scope")
		for x in self.variables: print x
		quit()						



	def loop_statement_handler(self, tree):
		while (["\n"] in tree): tree.remove(["\n"])
                while ([None] in tree): tree.remove([None])

		if tree[0] == "while": 	# sanity check
			my_block_prefix = self.genBlockId()
			my_loop_prefix = self.genBlockId()
			self.xStart.append("_" + my_loop_prefix + "_loop_header:\n")			
			self.expression_handler(tree[1]["value"]["value"])
			self.xStart.append("\tmov qword r11, [exprResolutionBuffer]\n")
                        self.xStart.append("\tcmp qword r11, 1\n")
                        self.xStart.append("\tjne _" + my_block_prefix + "_block_footer\n")                     
                        self.traverseParseTree(tree[2]) # parse block 
			self.xStart.insert(-1, "\tjmp _" + my_loop_prefix +"_loop_header\n")
			self.blockCount += 1	

	def condition_statement_handler(self, tree):
		while (["\n"] in tree): tree.remove(["\n"])
		while ([None] in tree): tree.remove([None])
		
		if tree[0] == "if" and len(tree) == 3:	#sanity check, tree: [if, expression, block]
			self.expression_handler(tree[1]["value"]["value"])
			my_block_prefix = self.genBlockId()
			self.xStart.append("\tmov qword r11, [exprResolutionBuffer]\n")
			self.xStart.append("\tcmp qword r11, 1\n")
			self.xStart.append("\tjne _" + my_block_prefix + "_block_footer\n")			
			self.traverseParseTree(tree[2])	#parse block 
				
				
	def declare_type(self, parseTree):
		if parseTree["type"] == "type_declaration": 
			
			myType = ""
			myName = ""
			myLiteral = ""

			decTree = parseTree["value"]
			defined = False 
			isArray = False 
			for token in decTree:
				if type(token) == dict:
					if token["type"] == "type_keyword":
						myType = token["value"]

					if token["type"] == "var_name":
						myName = token["value"]
						if "[" in myName and "]" in myName:
							isArray = True

					if token["type"] == "value":
						defined = True  
						myLiteral = token["value"]["value"]
			##
			##	ASSEMBLY VARIABLE FORMAT
			##	<scope id>_<type>_<name>
			##	<scope id>_<value>_<name>

			if isArray:
				if defined:
					myName, size = self.get_array_info(myName)
					myLiteral = self.clean_literal(myLiteral, myType, array=True)

					myName_val = self.blockId[-1] + "_val_" + myName 
					myName_type = self.blockId[-1] + "_type_" + myName

					# first byte array specifier 
					self.xStart.append("\tmov byte [" + myName_type + '], "a"\n')
					if myType == "char":    
                                                self.xStart.append("\tmov byte [" + myName_type + '+1], "c"\n')
                                                dataSize = 1
                                        	self.xBss.append("\t" + myName_val + ":\t resb " + str(size) + "\n")
					if myType == "int":     
                                                self.xStart.append("\tmov byte [" + myName_type + '+1], "i"\n')
                                                dataSize = 8 
						self.xBss.append("\t" + myName_val + ":\t resq " + str(size) + "\n")

					#need second byte for array (specifier, type)
					self.xBss.append("\t" + myName_type + ":\t resb 2\n")
						
					for index, element in enumerate(myLiteral):
						self.xStart.append("\tmov byte [" + myName_val + "+" + str(index*dataSize) + "]," + element + "\n")

					self.variables[self.blockId[-1]][myName] = {"type": myType, "array": False}

			else:
				if myType == "int":
					myName_val = self.blockId[-1] + "_val_" + myName 
					myName_type = self.blockId[-1] + "_type_" + myName
				
					self.xBss.append("\t" + myName_val + ":\t resq 1\n")
					self.xBss.append("\t" + myName_type + ":\t resb 1\n")
					
					self.xStart.append("\tmov byte [" + myName_type + '], "i"\n')
					
					if defined:
						myLiteral = self.clean_literal(myLiteral, myType)
						self.xStart.append("\tmov word [" + myName_val + "], " + myLiteral + "\n")
			
				if myType == "char":
					myName_val = self.blockId[-1] + "_val_" + myName 
					myName_type = self.blockId[-1] + "_type_" + myName

					self.xBss.append("\t" + myName_val + ":\t resb 1" "\n")
					self.xBss.append("\t" + myName_type + ":\t resb 1" "\n")
		
					self.xStart.append("\tmov byte [" + myName_type + '], "c"\n')
					
					if defined:
						myLiteral = self.clean_literal(myLiteral, myType)
						self.xStart.append("\tmov byte [" + myName_val + "], " + myLiteral + "\n")	

				
				self.variables[self.blockId[-1]][myName] = {"type": myType, "array": True}
			
		else: 
			print("!!! -- ERROR -- !!! - declare_type")
			return 

	def get_array_info(self, tree):
		if tree[1] == "[" and tree[-1] == "]":
			return tree[0], int(tree[2]["value"]["value"])


	def clean_literal(self, tree, myType, array=False):
		if array:
			literals = [] 
			if tree[0] == "[" and tree[-1] == "]":
				literals.append(self.clean_literal(tree[1]["value"]["value"], myType)) #grab first item 
				if type(tree[2]) == grako.contexts.Closure: #iterate over list of sucessive items
					for element in tree[2]:
						literals.append(self.clean_literal(element[1]["value"]["value"], myType))
				return literals
			else:
				print("ERROR: DID NOT FIND BRACES")
		else:
			if myType == "int":
				return tree
			if myType == "char":
				return """`""" + tree[1] + """`"""


	def expression_handler(self, tree):
		# this function need to accept a tree that contains an expression (or nested expressions)
		# and create the code necissary to place the result of the expression into the designated
		# expression resolution buffer. This way the result of the expression can be references 
		# later with other mothods 
		# 							exprResolutionBuffer 
		#print("= = = = = EXPRESSION HANDLER = = = = = ")
		#for x in tree: print "\t", x
		
		#sanity check 
		if tree[0] == "(" and tree[-1] == ")":
			operator = tree[2]["value"]
		
			###   What if these are literals? name resolver need to be able to recognize and handle literals ### 
			
			if tree[1]["value"]["type"] == "var_name":
				operand_1_Address, operand_1_type_Address, operand_1_type = self.name_resolver(tree[1]["value"]["value"])	
			
			if tree[3]["value"]["type"] == "var_name":
				operand_2_Address, operand_2_type_Address, operand_2_type = self.name_resolver( tree[3]["value"]["value"])
			#
			#	Modifications needed to support nested expressions 
			#

			self.xStart.append("\tmov qword [exprResolutionBuffer], 0\n")
			boolops = ["==", "!=", ">", "<", "<=", ">="]
			if operator in boolops: # Boolean operators 
				if "cl_bool_op" not in self.loadedFunctions:
                                	self.load_function_from_lib("cl_bool_op")
					self.loadedFunctions.append("cl_bool_op")		

				self.xStart.append("\tmov r11, [" + operand_1_Address + "];mov op1 to reg\n")
				self.xStart.append("\tmov r12, [" + operand_2_Address + "];mov op2 to reg\n")
				self.xStart.append("\tmov byte r13b, [" + operand_1_type_Address + "]; mov op1 type to reg\n")
				if operator == "==": 
					self.xStart.append("\tcall _cl_is_equal\n")	
				elif operator == "!=":
					self.xStart.append("\tcall _cl_is_not_equal\n")
				elif operator == ">":
					self.xStart.append("\tcall _cl_greater_than\n")
				elif operator == "<":                           
                                        self.xStart.append("\tcall _cl_less_than\n")
				elif operator == ">=":      
                                        self.xStart.append("\tcall _cl_greater_than_or_equal\n")
				elif operator == "<=":      
                                        self.xStart.append("\tcall _cl_less_than_or_equal\n")					

			elif operator == "+" or operator == "-" or operator == "*" or operator == "/": # Arithmetic operators 
				if "cl_arithmetic_op" not in self.loadedFunctions:
					self.load_function_from_lib("cl_arithmetic_op")
					self.loadedFunctions.append("cl_arithmetic_op")

				self.xStart.append("\tmov qword r11, [" + operand_1_Address + "];mov op1 to reg\n")
				self.xStart.append("\tmov qword r12, [" + operand_2_Address + "];mov op2 to reg\n")
				
				if operator == "+":
					self.xStart.append("\tcall _cl_addition\n")
				if operator == "-":
					self.xStart.append("\tcall _cl_subtraction\n")
				if operator == "*":
					self.xStart.append("\tcall _cl_multiplication\n")
				if operator == "/":
					self.xStart.append("\tcall _cl_division\n")

			else:
				#print "Expression operand type mismatch, return false or error?..."
				#print "\t", tree[2]["value"]
				pass

	def name_resolver(self, tree):
		# take in a var_name and return the proper constructed variable name + offset for 
		# the type and the value
	
		if type(tree) == unicode:
			scope_prefix = self.scope_resolver(tree)
			name_val = scope_prefix + "_val_" + tree
			name_type = scope_prefix + "_type_" + tree
			return name_val, name_type, self.variables[scope_prefix][tree]["type"]
		
		if type(tree) == list:
			
			if tree[1] == "[" and tree[3] == "]":
				if tree[2]["value"]["type"] == "literal":
					name = tree[0]
					scope_prefix = self.scope_resolver(name)
					index = int(tree[2]["value"]["value"])
					if name in self.variables[scope_prefix]:               	 
						myType = self.variables[scope_prefix][name]["type"]
						if myType == "char":
							multiplier = 1
						elif myType == "int":
							multiplier = 8 #qword
						return (scope_prefix + "_val_" + name + "+" + str(index*multiplier)), (scope_prefix + "_type_" + name + "+1"), myType
	
				if tree[2]["value"]["type"] == "var_name":
					index_address, index_type_address, index_type = self.name_resolver(tree[2]["value"]["value"])
					var_name = tree[0]
					my_type = ""
					scope_prefix = self.scope_resolver(var_name)
					if var_name in self.variables[scope_prefix]:
						my_type = self.variables[scope_prefix][var_name]["type"]
						if my_type == "char":
							multiplier = 1
						elif my_type == "int":
							multiplier = 8 
					
					my_type_address = scope_prefix + "_type_" + var_name + "+1"
					my_base_address = scope_prefix + "_val_" + var_name
					
					self.xStart.append("\tmov dword edi, [" + index_address + "]\n")
					self.xStart.append("\tmov r13, [" + my_base_address + " + edi *" + str(multiplier)  + "]\n")
					self.xStart.append("\tmov [indexBuffer], r13\n")
					
					return "indexBuffer", my_type_address, my_type 
				else:
					print("Error in name resolution finction: variable not in self.variables")
			else: 
				print("Error in name resolution function - no brackets found")
		else:
			print("Error in name resolution function")		


	def assign_value(self, tree):
		myName = ""
		mySource = "" # should be dict obj
		for x in tree:
			#print("\t" + str(x))
			if type(x) == dict:
				if x["type"] == "var_name": myName = x["value"]
				if x["type"] == "value": mySource = x["value"]
		
		if mySource["type"] == "literal": ## check type, clean, generate code 
			myLiteral = mySource["value"]
			if type(myLiteral) == list:
				myType = "char"
				typeCode = "c"
			if type(myLiteral) == unicode:
				myType = "int"
				typeCode = "i"
			myLiteral = self.clean_literal(myLiteral, myType)
			#need to verify type similarity of target and source
			
			myName_val,_,_ = self.name_resolver(myName)
			self.xStart.append("\tmov byte [" + myName_val + "], " + myLiteral + "\n")

		if mySource["type"] == "var_name": 
			mySourceAddress, sourceTypeAddress, sourceType = self.name_resolver(mySource["value"])
			myTargetAddress, targetTypeAddress, targetType = self.name_resolver(myName)
			
			#print "source type: \t", sourceType, targetType

			if True: # this is a good place to do some type checking 
				if sourceType == "int":
					self.xStart.append("mov r9, [" + mySourceAddress + "]\n")
					self.xStart.append("mov [" + myTargetAddress + "], r9\n")
			
				if sourceType == "char":
					self.xStart.append("mov r9b, [" + mySourceAddress + "]\n")
					self.xStart.append("mov byte [" + myTargetAddress + "], r9b\n")

			else:
				print("ERROR: invalid type addignment: " + sourceType + " to " + targetType) 
		
		if mySource["type"] == "expression":
			self.expression_handler(mySource["value"])
			myTargetAddress, targetTypeAddress, targetType = self.name_resolver(myName)	
			if targetType == "int" or targetType == "char":
				self.xStart.append("\tmov r11, [exprResolutionBuffer]\n")
				self.xStart.append("\tmov qword [" + myTargetAddress + "], r11\n")

		return 
	

	def call_function(self, tree):
		# will only work with single arg right now, additional infrastructure will be needed to handle multiple args 
		fName = tree[0]["value"]
		argName = tree[2]["value"]["value"]

		if fName in self.availableFunctions:
			if fName not in self.loadedFunctions:
				self.load_function_from_lib(fName)
				self.loadedFunctions.append(fName)

			valName, typeName,_ = self.name_resolver(argName)
			if fName in self.loadedFunctions:
				myTrigger = str(self.functionTriggers[fName])
				myTrigger = myTrigger.replace("<INSERT_VALUE>", valName)
				myTrigger = myTrigger.replace("<INSERT_TYPE>", typeName)
				myTrigger = myTrigger.split("\n")
				for line in myTrigger:
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

		idStr += effectiveAlphabet[temp]
		return idStr


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

			self.xBss.extend(bssTemp)	
			self.functionTriggers[fName] = startTemp
			self.functionCode.extend(primaryCode)

		except Exception as e:
			print(" === ERROR READING LIBRARY FUNCTION ===")
			print(e)
			return 

		# Need to strip empty lines at the end of this function 

	def assemble(self, outfile):
		##
		##	Send commands to command line to assemble and link the generated .asm file 
		##		
		p = pexpect.spawn("bash")
		p.expect(":~") ## expect most recent prompt 
		p.sendline("cd x86_tests")
		p.expect(":~")
		print p.before
		p.sendline("nasm -f elf64 -o test.o " + outfile + ".asm") #assemble code 
		p.expect(":~")
		print p.before
		p.sendline("ld test.o -o " + outfile)
		x = p.expect(":~")
		y = p.before
		print y
