types = ['integer','real','char','string','boolean']

class Context(object):
	def __init__(self):
		self.variables = {}
	
	def has_var(self,name):
		return name in self.variables
	
	def get_var(self,name):
		return self.variables[name]
	
	def set_var(self,name,typ):
		self.variables[name] = typ

contexts = []
functions = {
	'write':['string'],
	'writeln':['string'],
	'writeint':['integer']
}

def has_var(var):
	for c in contexts[::-1]:
		if c.has_var(var):
			return True
	return False

def get_var(var):
	for c in contexts[::-1]:
		if c.has_var(var):
			return c.get_var(var)
	raise Exception, "Variable %s is referenced before assignment" % var
	
def set_var(var,typ):
	now = contexts[-1]
	if now.has_var(var):
		raise Exception, "Variable %s already defined" % var
	else:
		now.set_var(var,typ)
	
def get_params(node):
	if node.type == "parameter":
		return [node.args[0].args[0].type ]
	else:
		l = []
		for i in node.args:
			l.extend(get_params(i))
		return l

def is_node(n):
	return hasattr(n,"type")

def check(node):
	if not is_node(node):
		if hasattr(node,"__iter__") and type(node) != type(""):
			for i in node:
				check(i)
		else:
			return node
	else:
		if node.type in ['identifier']:
			return node.args[0]
			
		elif node.type in ['var_list','statement_list']:
			return check(node.args)
			
		elif node.type in ["program","block"]:
			contexts.append(Context())
			check(node.args)
			contexts.pop()
			
		elif node.type == "var":
			var_name = node.args[0].args[0]
			var_type = node.args[1].args[0]
			set_var(var_name, var_type)
			
		elif node.type in ["function_call","function_call_inline"]:
			fname = node.args[0].args[0].lower()
			if fname not in functions:
				raise Exception, "Function %s is not defined." % fnames
			if len(node.args) > 1:
				args = get_params(node.args[1])
			else:
				args = []
			vargs = functions[fname]
		
			if len(args) != len(vargs):
				raise Exception, "Function %s is expecting %d parameters and got %d" % (fname, len(vargs), len(args))
			else:
				for i in range(len(vargs)):
					if vargs[i] != args[i]:
						raise Exception, "Parameter #%d passed to function %s should be of type %s and not %s" % (i+1,fname,vargs[i],args[i])
				
				
		else:
			print node.type