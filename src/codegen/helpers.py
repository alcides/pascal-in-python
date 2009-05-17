from llvm.core import *
import ptypes as types


def c_int(val):
	return Constant.int(types.integer,val)

def c_string(context,val):
	""" Creates a string for LLVM """
	str = context.add_global_variable(Type.array(types.int8, len(val) + 1), "")
	str.initializer = Constant.stringz(val)
	return str
	
def pointer(block,val):
	""" Returns the pointer for a value """
	return block.gep(val,(  c_int(0), c_int(0) ))
	
	
def add_stdio(mod):
	""" Adds stdio functions to a module """
	return {
			"printf": mod.add_function(
		types.function(types.void, (Type.pointer(types.int8, 0),), 1), "printf")
	}
	
def create_main(mod):
	""" Returns a main function """
	return mod.add_function(
types.function(types.integer, (Type.pointer(types.int8, 0),), 1), "main")