from llvm import *
from llvm.core import *
import ptypes as types
from codegen import *
from ast import Node

# http://mdevan.nfshost.com/llvm-py/userguide.html#install

class Writer(object):

	def __init__(self):
		self.functions={}

	def descend(self,node):
		self(node)


	def __call__(self,ast):
		
		if ast is not Node:
			return "error"
		
		if ast.type == "program":
			mod_name = ast.args[0]
			if not mod_name:
				mod_name = "pascal_program"
			
			self.module = Module.new(mod_name)
			stdio = add_stdio(self.module)
			for f in stdio:
				self.functions[f] = stdio[f]
			
			self.descend(ast.args[1])
			
		elif ast.type == "block":
			self.descend(ast.args[0]) # Var
			self.descend(ast.args[1]) # Statement
			
		return self.module
		

if __name__ == '__main__':
	m = Module.new('my_module')
	
	stdio = add_stdio(m)
	
	printf = stdio['printf']
	
	
	ty_func = Type.function(types.integer, [])
	f = m.add_function(ty_func, "main1")
	bb = f.append_basic_block("entry")
	builder = Builder.new(bb)
	
	zero = Constant.int(types.integer, 1)
	r = zero.add(Constant.int(types.integer,2))
	builder.ret(r)
	
	from t import *
	m = mod
	
	tpointer = Type.pointer(Type.pointer(types.int8, 0), 0)	
	ft = Type.function(types.integer,[ types.integer, tpointer  ] )
	main = m.add_function( ft, "main"   )
	bb = main.append_basic_block("entry")
	builder = Builder.new(bb)
	builder.call(printf,   (
		pointer(builder,c_string(mod, "hell yeah")),
	
	))
	builder.ret(c_int(5))
	
	print m
	if True:# m.verify() is None:
		m.to_bitcode(file("test.bc", "w"))
		import os
		#os.system("llvm-as test.bc | opt -std-compile-opts -f > test_opt.bc")
		os.system("lli test.bc > success.txt")
		#os.system("llc test.bc -o program.c")
		#os.system("gcc program.c -o a.out")
	else:
		print "error"