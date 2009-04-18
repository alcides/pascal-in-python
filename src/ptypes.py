from llvm.core import *

# auxiliary
void = Type.void()
boolean = Type.int(1)

integer = Type.int()
real  = Type.double()
char = Type.int()
string = lambda x: Type.array( integer, x )

def function(rt,*args):
	return Type.function(rt, args)
	
def procedure(*args):
	return Type.function(void, args)