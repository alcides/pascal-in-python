from llvm.core import *

# auxiliary
void = Type.void()
boolean = Type.int(1)
int8 = Type.int(8)

integer = Type.int()
real  = Type.double()
char = Type.int()
string = lambda x: Type.array( integer, x )

function = Type.function

def procedure(*args):
	return Type.function(void, args)