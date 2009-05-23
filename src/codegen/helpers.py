from llvm.core import *
import ptypes as types


def compare(sign,v1,v2):
	""" [">",">=","=","<=","<","<>"] """
	if sign == ">":
		i_cod = IPRED_UGT
		f_cod = RPRED_OGT
	elif sign == ">=":
		i_cod = IPRED_UGE
		f_cod = RPRED_OGE
	elif sign == "=":
		i_cod = IPRED_EQ
		f_cod = RPRED_OEQ
	elif sign == "<=":
		i_cod = IPRED_ULE
		f_cod = RPRED_OLE
	elif sign == "<":
		i_cod = IPRED_ULT
		f_cod = RPRED_OLT
	elif sign == "<>":
		i_cod = IPRED_NE
		f_cod = RPRED_ONE
	else:
		return c_boolean(False)
	
	if v1.type == types.integer:
		return v1.icmp(i_cod, v2)
	elif v1.type == types.real:
		return v1.fcmp(f_code, v2)
	else:
		return c_boolean(False)
	

def c_boolean(val):
	if val:
		return c_int(1).icmp(IPRED_UGT,c_int(0))
	else:
		return c_int(0).icmp(IPRED_UGT,c_int(1))

def c_int(val):
	return Constant.int(types.integer,val)

def c_real(val):
	return Constant.real(types.real, val)

def c_string(context,val,name=""):
	""" Creates a string for LLVM """
	str = context.add_global_variable(Type.array(types.int8, len(val) + 1), name)
	str.initializer = Constant.stringz(val)
	return str
	
def pointer(block,val):
	""" Returns the pointer for a value """
	return block.gep(val,(  c_int(0), c_int(0) ))
	
	
def add_stdio(mod):
	""" Adds stdio functions to a module """
	return {
		"printf": mod.add_function(types.function(types.void, (Type.pointer(types.int8, 0),), 1), "printf"),
		"writeln": create_write(mod,ln=True),
		"write": create_write(mod),
		"writeint": create_writeint(mod)		
	}
	
def create_main(mod):
	""" Returns a main function """
	
	tpointer = Type.pointer(Type.pointer(types.int8, 0), 0)	
	ft = Type.function(types.integer,[ types.integer, tpointer  ] )
	return mod.add_function(ft, "main")


def create_write(mod,ln=False):
	""" Creates a stub of println """
	
	printf = mod.get_function_named("printf")
	
	string_pointer = Type.pointer(types.int8, 0)
	
	f = mod.add_function(
		types.function(types.void, (string_pointer,) )
	, "writeln")
	bb = f.append_basic_block("entry")	
	builder = Builder.new(bb)
	builder.call(printf,   (
		f.args[0],
	))
	
	if ln:
		builder.call(printf,   (
			pointer(builder, c_string(mod,"\n")),
		))
	builder.ret_void()
	return f

def create_writeint(mod):
	printf = mod.get_function_named("printf")
	
	funcType = Type.function(Type.void(), [Type.int(32)])  
	printInt = mod.add_function(funcType, 'writeint')  

	bb = printInt.append_basic_block('bb')  
	b = Builder.new(bb)  
	
	stringConst = c_string(mod,"%d\n")
	stringConst = pointer(b,stringConst)
	
	b.call(printf,[stringConst,printInt.args[0]])
	b.ret_void()
	return printInt;
	