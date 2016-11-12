
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
		

	def preprocessing(self):
                temp = []
                skip = False
                for i, line in enumerate(self.sourceText):
                        if skip:
                                skip = False
                                continue
                        if "&" in line:
                                tempStr = line.replace("&", test[i+1].replace("\n", ""))
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
			print("\n================== Syntax Tree  ==================")
                	print(json.dumps(self.parseTree, indent=2)) # ASTs are JSON-friendy
			print()


