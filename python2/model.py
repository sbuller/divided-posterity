class Model:
	def __init__(self, backend):
		self.storage = backend() #Instatiate an instance of the class 'backend'
		self.backend = backend

	def set_storage(self, backend):
		if not self.backend == backend:
			#Some transactiony goodness might be called for here.
			storage = backend()
			#storage.update(self.storage)
			oldstorage = self.storage
			self.storage = storage
			del oldstorage

class Hero(Model):
	def __init__(self):
		pass

	def set_storage(self, storage):
		self.storage = storage

	def get_location(self):
		pass

	def travel(self, destination):
		pass
