import sys

from llvm import *
from llvm.core import *

import ptypes as types
from helpers import *
from ast import Node
from context import Context


# http://mdevan.nfshost.com/llvm-py/userguide.html#install


class Writer(object):

	def __init__(self):
		self.functions={}
		self.contexts = []

	def descend(self,node):
		return self(node)

	def __call__(self,ast):
		
		if ast.__class__ != Node:
			return ast
			
		if ast.type == "program":
			mod_name = self.descend(ast.args[0])
			if not mod_name:
				mod_name = "pascal_program"
			
			self.module = Module.new(mod_name)
			stdio = add_stdio(self.module)
			for f in stdio:
				self.functions[f] = stdio[f]
			
			main = create_main(self.module)
			block = Builder.new(main.append_basic_block("entry"))
			
			self.contexts.append(Context(block))
			self.descend(ast.args[1])
			
			block.ret(c_int(0))
			
			return self.module
			
		elif ast.type == "block":
			self.descend(ast.args[0]) # Var
			self.descend(ast.args[1]) # Function def
			self.descend(ast.args[2]) # Statement
		
		elif ast.type == "var_list" or ast.type == "statement_list":
			for son in ast.args:
				self.descend(son)
				
		elif ast.type == "var":
			var_name = ast.args[0]
			var_type_name = self.descend(ast.args[1])
			var_type = types.translation[var_type_name]
			var_value = types.defaults[var_type_name]
			
			builder = self.contexts[-1].get_builder()
			v = builder.alloca(var_type)
			builder.store(c_int(var_value),v)
			
		elif ast.type == "type":
			return ast.args[0]
			
		elif ast.type == "identifier":
			return ast.args[0]
			
		elif ast.type == "function_call":
			builder = self.contexts[-1].get_builder()
			
			function_name = self.descend(ast.args[0])
			function = self.module.get_function_named(function_name)
			
			arguments = []
			
			if ast.args[1]:
				arguments = self.descend(ast.args[1])
					
			builder.call(function,arguments)
			
		elif ast.type == "parameter":
			c = ast.args[0]
			if c.type == "identifier":
				label = self.descend(ast.args[0])
				c = self.contexts[-1].get_variable(label)
			else:
				c = self.descend(ast.args[0])
			return [c]
			
		elif ast.type == "element":
			return self.descend(ast.args[0])
			
		elif ast.type == "string":
			b = self.contexts[-1].get_builder()
			s = c_string(self.module,ast.args[0])
			return pointer(b,s)
			
		elif ast.type == "integer":
			return c_int(int(ast.args[0]))
			
		else:
			print "unknown:", ast.type
			sys.exit()
