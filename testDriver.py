import codeGenerator 
#testFiles = [1,2,3,4,5,6,7,8,9,10,11,12,13]
testFiles = [1]


for x in testFiles:
	filename = "tests/cgt" + str(x).replace("\n", "")
	myCodeGen = codeGenerator.codeGenerator(filename)
