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
	
	
translation = {
	"INTEGER": integer,
	"REAL": real,
	"CHAR": char
}

class ReverseDict(object):
	def __init__(self,dic):
		self.dic = dic
	def __getitem__(self,p):
		for k in self.dic:
			if self.dic[k] == p:
				return k
				
reverse_translation = ReverseDict(translation)
				
defaults = {
	"INTEGER": 0,
	"REAL": 0.0,
	"CHAR": '_'
}