import sys, os
from subprocess import Popen, PIPE

from ply import yacc,lex

from tokens import *
from rules import *
from semantic import *
from codegen.builder import *

def get_input(file=False):
	if file:
		f = open(file,"r")
		data = f.read()
		f.close()
	else:
		data = ""
		while True:
			try:
				data += raw_input() + "\n"
			except:
				break
	return data

def main(options={},filename=False):
	logger = yacc.NullLogger()
	yacc.yacc(debug = logger, errorlog= logger )
	
	data = get_input(filename)
	ast =  yacc.parse(data,lexer = lex.lex(nowarn=1))	
	
	if options.graph:
		from codegen.graph import graph
		graph(ast, filename)
	
	try:
		check(ast)
	except Exception, e:
		print "Error: %s" % e
		sys.exit()
	
	try:
		o = Writer()(ast)
	except Exception, e:
		print "Error(2): %s" % e
		sys.exit()

	if not hasattr(o,"ptr"):
		print "Error compiling"
		sys.exit()
		
	if options.verbose:
		print o
		if options.run:
			print 20*"-" + " END " + 20*"-"
		
	if options.run:
		
		# hack
		from llvm.core import _core
		bytecode = _core.LLVMGetBitcodeFromModule(o.ptr)
		
		p = Popen(['lli'],stdout=PIPE, stdin=PIPE)
		sys.stdout.write(p.communicate(bytecode)[0])
	else:		
		o.to_bitcode(file("tmp/middle.bc", "w"))
		#os.system("llvm-as tmp/middle.bc | opt -std-compile-opts -f > tmp/optimized.bc")
		os.system("llc -f -o=tmp/middle.s tmp/middle.bc")
		os.system("gcc -o %s tmp/middle.s" % options.filename)
	
	
if __name__ == '__main__':
	main()