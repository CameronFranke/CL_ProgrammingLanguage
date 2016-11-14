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

		self.xSourceFile = "x86_tests/clTest.asm"
		self.xData = []
		self.xText = []
		self.xStart = []

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
						myLiteral = self.build_literal(token["value"])
		
			#print myType
			#print myName
			#print myLiteral
			self.xData.append(myName + " db " + myLiteral)
		
		else: 
			print("!!! -- ERROR -- !!! - declare_type")
			return 
	

	def build_literal(self, tree):
		if type(tree) == dict:
			if tree["type"] == "literal":
				return tree["value"]


	
	def write_x86_source(self):
		with open(self.xSourceFile, "w+") as s:
		
			if len(self.xData) > 0:
				s.write("section .data\n")
				for x in self.xData:
					s.write("\t" + str(x) + "\n")	

			s.write("section .data\n")
			s.write("\tglobal _start\n")
			for x in self.xText:
				s.write("\t" + str(x) + "\n")

			s.write("_start:\n")
			for x in self.xStart:
				s.write("\t" + str(x) + "\n")
			
			s.write("\tmov rax, 60\n")
			s.write("\tmov rdi, 0\n")
			s.write("\tsyscall\n")





































