#This can be replaced by a simple dict. It will serve as a template for other
#storage modules.
class MemStorage:
	def __init__(self):
		pass

	def __getitem__(self,name):
		return self.__dict__[name]

	def __setitem__(self,name,value):
		self.__dict__[name] = value

	def __del__(self):
		pass
