from llvm import *
from llvm.core import *
import ptypes as types
from helpers import *
from ast import Node

# http://mdevan.nfshost.com/llvm-py/userguide.html#install

class Writer(object):

	def __init__(self):
		self.functions={}

	def descend(self,node):
		return self(node)


	def __call__(self,ast):
		
		if ast.__class__ != Node:
			return "Some error building: ", ast
		
		if ast.type == "program":
			mod_name = ast.args[0]
			if not mod_name:
				mod_name = "pascal_program"
			
			self.module = Module.new(mod_name)
			stdio = add_stdio(self.module)
			for f in stdio:
				self.functions[f] = stdio[f]
			
			self.descend(ast.args[1])
			
			return self.module
			
		elif ast.type == "block":
			self.descend(ast.args[0]) # Var
			self.descend(ast.args[1]) # Statement
		
		elif ast.type == "var_list":
			for son in ast.args:
				self.descend(son)
				
		elif ast.type == "var":
			var_name = ast.args[0]
			var_value = self.descend(ast.args[1])
			print var_name, var_value
		
		elif ast.type == "type":
			return ast.args[0]
		
		else:
			print ast.type
