import clparser
import json

testFiles = [6]


parser = clparser.UnknownParser(parseinfo=True)

for x in testFiles:
	x = "tests/pt" + str(x)
	with open(x, "r") as test: 
		test = test.readlines()
		
	# # #		PRE PROCESSING 		# # #

		temp = []
		skip = False 
		for i, line in enumerate(test):
			if skip:
				skip = False
				continue
			if "&" in line: 
				tempStr = line.replace("&", test[i+1].replace("\n", ""))
				skip = True
				temp.append(tempStr)
			else: 
				temp.append(line)
		test = ""
		for x in temp:
			test += x
		
		test = "@@@\n" + test + "\n@@@"
		print test

	# # #		PRE PROCESSING		# # #
		
		ast = parser.parse(test, rule_name='program', semantics=clparser.UnknownSemantics())
		print("====================================")
		print(ast)
		print("====================================")
		#print([method for method in dir(ast) if callable(getattr(ast, method))])
		#print("====================================")

		print(json.dumps(ast, indent=2)) # ASTs are JSON-friendy
		with open("ast.json", "w+") as outfile:
			json.dump(ast, outfile, indent=4)
