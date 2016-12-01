import codeGenerator 
import sys

if len(sys.argv) > 1:
	x = sys.argv[1]
else:
	x = 11 # will default to hello world 

filename = "tests/cgt" + str(x).replace("\n", "")
myCodeGen = codeGenerator.codeGenerator(filename)
myCodeGen.traverseParseTree(myCodeGen.parseTree)
myCodeGen.write_x86_source()
myCodeGen.assemble("clTest")
