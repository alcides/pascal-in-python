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
	'write':[("a",'string')],
	'writeln':[("a",'string')],
	'writeint':[("a",'integer')],
	'writereal':[("a",'real')]
}

def check_if_function(var):
	if var in functions:
		raise Exception, "A function called %s already exists" % var
		
def has_var(varn):
	var = varn.lower()
	check_if_function(var)
	for c in contexts[::-1]:
		if c.has_var(var):
			return True
	return False

def get_var(varn):
	var = varn.lower()
	for c in contexts[::-1]:
		if c.has_var(var):
			return c.get_var(var)
	raise Exception, "Variable %s is referenced before assignment" % var
	
def set_var(varn,typ):
	var = varn.lower()
	check_if_function(var)
	now = contexts[-1]
	if now.has_var(var):
		raise Exception, "Variable %s already defined" % var
	else:
		now.set_var(var,typ)
	
def get_params(node):
	if node.type == "parameter":
		if is_node(node.args[0].args[0]):
			t = node.args[0].args[0]
		if t.type == 'identifier':
			return [get_var(t.args[0])]
		else:
			return [t.type]
	else:
		l = []
		for i in node.args:
			l.extend(get_params(i))
		return l
		
def flatten(n):
	if not is_node(n): return [n]
	if not n.type.endswith("_list"):
		return [n]
	else:
		l = []
		for i in n.args:
			l.extend(flatten(i))
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
		if node.type == ['element']:
			return get_var(node.args[0].args[0])
		
		elif node.type in ['identifier']:
			return node.args[0]
			
		elif node.type in ['var_list','statement_list','function_list']:
			return check(node.args)
			
		elif node.type in ["program","block"]:
			contexts.append(Context())
			check(node.args)
			contexts.pop()
			
		elif node.type == "var":
			var_name = node.args[0].args[0]
			var_type = node.args[1].args[0]
			set_var(var_name, var_type)
			
		elif node.type in ['function','procedure']:
			head = node.args[0]
			name = head.args[0].args[0].lower()
			check_if_function(name)
			
			if len(head.args) == 1:
				args = []
			else:
				args = flatten(head.args[1])
				args = map(lambda x: (x.args[0].args[0],x.args[1].args[0]), args)
			functions[name] = args
			
			
			contexts.append(Context())
			for i in args:
				set_var(i[0],i[1])
			check(node.args[1])
			contexts.pop()
			
		elif node.type in ["function_call","function_call_inline"]:
			fname = node.args[0].args[0].lower()
			if fname not in functions:
				raise Exception, "Function %s is not defined" % fname
			if len(node.args) > 1:
				args = get_params(node.args[1])
			else:
				args = []
			vargs = functions[fname]
		
			if len(args) != len(vargs):
				raise Exception, "Function %s is expecting %d parameters and got %d" % (fname, len(vargs), len(args))
			else:
				for i in range(len(vargs)):
					if vargs[i][1].lower() != args[i].lower():
						raise Exception, "Parameter #%d passed to function %s should be of type %s and not %s" % (i+1,fname,vargs[i],args[i])
				
				
		else:
			print "semantic missing:", node.type