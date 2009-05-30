from llvm.core import *

class Context(object):
	def __init__(self,current,builder = False):
		self.current = current
		if not builder:
			self.builder = Builder.new(self.current)
		else:
			self.builder = builder
		
		self.variables = {}
		self.params = {}
		
	def has_variable(self,name):
		return name in self.variables or name in self.params
		
	def set_variable(self,name,value):
		self.variables[name] = value
		
	def set_param(self,name,value):
		self.params[name] = value
		
	def get_variable(self,name):
		if name in self.params:
			return self.params[name]
		if name in self.variables:
			return self.variables[name]
		raise Exception, "Variable %s doesn't exist" % name
			
	def get_builder(self):
		return self.builder