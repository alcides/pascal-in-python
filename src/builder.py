from llvm import *
from llvm.core import *
import ptypes as types

# http://mdevan.nfshost.com/llvm-py/userguide.html#install

class Writer(object):

	def descend(self,node):
		pass


	def __call__(self,ast):
		if ast.type == "program":
			self.module = Module.new(ast.args[0])
			self.descend(ast.args[1])
