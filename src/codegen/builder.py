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
		self.counter = 0
		
	def get_var(self,name):
		for c in self.contexts[::-1]:
			if c.has_variable(name):
				return c.get_variable(name)
		raise Exception, "Variable %s doesn't exist" % name
		
	def set_var(self,name,value):
		self.contexts[-1].set_variable(name,value)

	def get_builder(self):
		return self.contexts[-1].get_builder()
		
	def get_current(self):
		return self.contexts[-1].current
		
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
			
			self.contexts.append(Context(main,block))
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
			var_name = self.descend(ast.args[0])
			var_type_name = self.descend(ast.args[1])
			var_type = types.translation[var_type_name]
			var_value = types.defaults[var_type_name]
			
			
			builder = self.get_builder()
			
			v = builder.alloca(var_type)
			
			builder.store(c_int(var_value),v)
			self.set_var(var_name,v)
			
		elif ast.type == "type":
			return str(ast.args[0]).upper()
			
		elif ast.type == "identifier":
			return str(ast.args[0]).lower()
			
		elif ast.type == "function_call":
			builder = self.get_builder()
			
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
				c = self.get_var(label)
			else:
				c = self.descend(ast.args[0])
			return [c]
			
		elif ast.type == "assign":
			builder = self.get_builder()
			varName = self.descend(ast.args[0])
			value = self.descend(ast.args[1])
			ref = self.get_var(varName)
			builder.store(value, ref)
        
		elif ast.type == "if":
			now = self.get_current()
			builder = self.get_builder()
			
			#if
			cond = self.descend(ast.args[0])
			
			# the rest
			self.counter += 1
			tail = now.append_basic_block("tail_" + str(self.counter))
			
			# then
			then_block = now.append_basic_block("if_" + str(self.counter))
			self.contexts.append( Context(then_block)  )
			self.descend(ast.args[1])
			self.get_builder().branch(tail)
			self.contexts.pop()
			
			# else
			else_block = now.append_basic_block("else_" + str(self.counter))
			self.contexts.append( Context(else_block)  )
			if len(ast.args) > 2:
				self.descend(ast.args[2])
			self.get_builder().branch(tail)				
			self.contexts.pop()
			
			
			builder.cbranch(cond,then_block,else_block)
			self.contexts.append(Context(tail))
			
				

		elif ast.type == "sign":
			return ast.args[0]

		elif ast.type == "op":
			sign = self.descend(ast.args[0])
			v1 = self.descend(ast.args[1])
			v2 = self.descend(ast.args[2])
			
			builder = self.get_builder()
			
			if sign == "+":
				return builder.add(v1, v2)
			elif sign == "-":
				return builder.sub(v1, v2)
			elif sign == "*":
				return builder.mul(v1, v2)
			elif sign == "/":
				return builder.fdiv(v1, v2)
			elif sign == "mod":
				return builder.sdiv(v1, v2)
			elif sign in [">",">=","=","<=","<","<>"]:
				return compare(sign,v1,v2)
			else:
				print sign	
				
				
		elif ast.type == "element":
			builder = self.get_builder()
			
			e = ast.args[0]
			if e.type == "identifier":
				ref = self.get_var(self.descend(e))
				return builder.load(ref)
			else:
				return self.descend(ast.args[0])
			
		elif ast.type == "string":
			b = self.get_builder()
			s = c_string(self.module,ast.args[0])
			return pointer(b,s)
			
		elif ast.type == "integer":
			return c_int(int(ast.args[0]))
			
		elif ast.type == "real":
			return c_real(float(ast.args[0]))
			
		else:
			print "unknown:", ast.type
			sys.exit()
