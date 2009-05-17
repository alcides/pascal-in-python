from llvm import *
from llvm.core import *
import ptypes as types
from helpers import *

m = Module.new('my_module')

stdio = add_stdio(m)

printf = stdio['printf']


ty_func = Type.function(types.integer, [])
f = m.add_function(ty_func, "main1")
bb = f.append_basic_block("entry")
builder = Builder.new(bb)

tpointer = Type.pointer(Type.pointer(types.int8, 0), 0)	
ft = Type.function(types.integer,[ types.integer, tpointer  ] )
main = m.add_function( ft, "main"   )
bb = main.append_basic_block("entry")
builder = Builder.new(bb)
builder.call(printf,   (
	pointer(builder,c_string(m, "hell yeah")),

))
builder.ret(c_int(5))

print m
if True:# m.verify() is None:
	m.to_bitcode(file("test.bc", "w"))
	import os
	#os.system("llvm-as test.bc | opt -std-compile-opts -f > test_opt.bc")
	#os.system("lli test.bc > success.txt")
	#os.system("llc test.bc -o program.c")
	#os.system("gcc program.c -o a.out")
else:
	print "error"