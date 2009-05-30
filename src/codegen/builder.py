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

	def set_param(self,name,value):
		self.contexts[-1].set_param(name,value)
		
	def get_builder(self):
		return self.contexts[-1].get_builder()
		
	def get_current(self):
		return self.contexts[-1].current
		
	def get_function(self):
		for c in self.contexts[::-1]:
			if c.current.__class__ == Function:
				return c.current
		
	def descend(self,node):
		return self(node)

	def __call__(self,ast):
		
		if ast.__class__ != Node:
			return ast
			
		print ast.type, id(ast)
			
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
			
			self.get_builder().ret(c_int(0))
			
			return self.module
			
		elif ast.type == "block":

			self.descend(ast.args[0]) # Var
			self.descend(ast.args[1]) # Function def
			self.descend(ast.args[2]) # Statement
		
		elif ast.type in ["var_list","statement_list","function_list"]:
			for son in ast.args:
				self.descend(son)
				
		elif ast.type == "var":
			var_name = self.descend(ast.args[0])
			var_type_name = self.descend(ast.args[1])
			builder = self.get_builder()
			v = var_init(builder, var_name, var_type_name)
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
			
			if len(ast.args) > 1:
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
			return varName
			
		elif ast.type in ['procedure','function']:
			
			
			def get_params(node):
				""" Return a list of tuples of params """
				if node.type == 'parameter':
					return [(self.descend(node.args[0]), types.translation[self.descend(node.args[1])])]
				else:
					l = []
					for p in node.args:
						l.extend(get_params(p))
					return l
				
			
			if ast.type == 'procedure':
				return_type = types.void
			else:
				pass
				
			name = self.descend(ast.args[0].args[0])
			if len(ast.args) > 1:
				params = get_params(ast.args[0].args[1])
			else:
				params = []
			code = ast.args[1]
			
			ftype = types.function(return_type,[ i[1] for i in params ])
			f = Function.new(self.module, ftype, name)
			
			self.contexts.append(Context( f.append_basic_block("entry") ))
			b = self.get_builder()
			for i,p in enumerate(params):
				x = f.args[i]; x.name = p[0]
				self.set_param(p[0],x)
				
			self.descend(code)
			if ast.type == 'procedure':
				self.get_builder().ret_void()
			self.contexts.pop()
		
        

		elif ast.type == "while":
			self.counter += 1
			now = self.get_function()
			builder = self.get_builder()
			
			
			loop = now.append_basic_block("loop_%d" % self.counter)			
			body = now.append_basic_block("body_%d" % self.counter)
			tail = now.append_basic_block("tail_%d" % self.counter)

			# do while code
			self.contexts.append(Context(loop))
			b = self.get_builder()
			cond = self.descend(ast.args[0])
			b.cbranch(cond,body,tail)
			self.contexts.pop()
			
			self.contexts.append(Context(body))
			b = self.get_builder()
			self.descend(ast.args[1])
			# repeat
			b.branch(loop)
			self.contexts.pop()
			
			# start loop
			builder.branch(loop)
			
			# continue
			self.contexts.append(Context(tail))
			
		elif ast.type == "repeat":
			cond = ast.args[1]
			body = ast.args[0]
			
			while_b = Node('while',cond,body)
			final = Node('statement_list',body,while_b)
			return self.descend(final)
			
		elif ast.type == "for":
			
			direction = self.descend(ast.args[1])
			limit = ast.args[2]
			builder = self.get_builder()
			
			# var declaration
			varname = self.descend(ast.args[0].args[0])
			vartype = "INTEGER"
			v = var_init(builder, varname, vartype)
			self.set_var(varname,v)
			
			# var init
			variable = self.descend(ast.args[0])
			
			# cond
			var1 = Node('element',Node('identifier',varname))
			var1_name = Node('identifier',varname)

			sign = Node('sign',(direction == "to") and '<=' or '>=')
			comp = Node('op',sign,var1,limit)
			
			# body
			op = Node('sign',(direction == "to") and '+' or '-')
			varvalue = Node('op',op,var1,Node('element',Node('integer',1)))
			increment = Node('assign',var1_name,varvalue)
			
			body = Node('statement_list',ast.args[3],increment)
			
			# do while
			while_block = Node('while',comp,body)			
			
			self.descend(while_block)
			
			
		elif ast.type == "if":
			now = self.get_function()
			builder = self.get_builder()
			
			#if
			cond = self.descend(ast.args[0])
			
			# the rest
			self.counter += 1
			tail = now.append_basic_block("tail_%d" % self.counter)
			
			# then
			then_block = now.append_basic_block("if_%d" % self.counter)
			self.contexts.append( Context(then_block)  )
			self.descend(ast.args[1])
			b = self.get_builder()
			b.branch(tail)
			b.position_at_end(tail)
			self.contexts.pop()
			
			# else
			else_block = now.append_basic_block("else_%d" % self.counter)
			self.contexts.append( Context(else_block)  )
			if len(ast.args) > 2:
				self.descend(ast.args[2])
			b = self.get_builder()
			b.branch(tail)
			b.position_at_end(tail)
			self.contexts.pop()
			
			builder.cbranch(cond,then_block,else_block)
			self.contexts.append(Context(tail))
				

		elif ast.type in ["sign","and_or"]:
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
				return compare(sign,v1,v2,builder)
			elif sign == "and":
				return builder.and_(v1,v2)
			elif sign == "or":
				return builder.or_(v1,v2)
			else:
				print sign	
				
				
		elif ast.type == "element":
			builder = self.get_builder()
			
			e = ast.args[0]
			if e.type == "identifier":
				ref = self.get_var(self.descend(e))
				if ref.__class__ == Argument:
					return ref
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
