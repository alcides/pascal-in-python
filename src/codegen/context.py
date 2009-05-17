class Context(object):
	def __init__(self,builder,parent=False):
		self.builder = builder
		self.variables = []
		self.parent = parent
		
	def set_variable(self,name,value):
		self.variables[name] = vale
		
	def get_variable(self,name):
		if name in self.variables:
			return self.variables[name]
		if self.parent:
			return self.parent.get_variable(name)
		else:
			return None
			
	def get_builder(self):
		return self.builder