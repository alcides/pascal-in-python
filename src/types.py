class PObject(object):
	self.value = None
	self.type = "null"

class PString(PObject):
	def __init__(self,s):
		self.type = "STRING"
		self.value = str(s)
		
class PChar(PObject):
	def __init__(self,s):
		self.type = "CHAR"
		self.value = str(s)[0]

class PReal(PObject):
	def __init__(self,s):
		self.type = "REAL"
		self.value = float(s)
		
class PInteger(PObject):
	def __init__(self,s):
		self.type = "INTEGER"
		self.value = int(s)