import clparser
import json

testFiles = [1,2,3,4,5,6,7,8,9,10,11,12,13]


parser = clparser.UnknownParser()
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
		
		ast = parser.parse(test, rule_name='program')
		print(ast)
		print(json.dumps(ast, indent=2)) # ASTs are JSON-friendy
		with open("ast.json", "w+") as outfile:
			json.dump(ast, outfile, indent=4)
