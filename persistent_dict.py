
NO_VALUE = object()

class PersistentDict(object):
	'''
	>>> d = PersistentDict(dict(a=10, b=20))
	>>> sorted(d.items())
	[('a', 10), ('b', 20)]
	>>> d2 = d.set('c', 30)
	>>> sorted(d2.items())
	[('a', 10), ('b', 20), ('c', 30)]
	>>> d3 = d2.delete('b')
	>>> sorted(d3.items())
	[('a', 10), ('c', 30)]
	>>> sorted(d.items()) # previous version is intact
	[('a', 10), ('b', 20)]
	'''

	__slots__ = [
		'successor',
		'data',		# either dict contents or diff (in case successor is not None)
		]
	def __init__(self, d=None):
		self.successor = None
		if d is None:
			self.data = {}
		else:
			self.data = dict(d)

	def reroot(self):
		succ = self.successor
		if succ is None:
			return

		succ.reroot()

		data = succ.data
		new_diff = {}
		for k, v in self.data.items():
			new_diff[k] = data.get(k, NO_VALUE)
			if v is NO_VALUE:
				del data[k]
			else:
				data[k] = v
		succ.data = new_diff
		succ.successor = self
		self.data = data
		self.successor = None

	def get(self, key, default=None):
		self.reroot()
		return self.data.get(key, default)

	def __getitem__(self, key):
		self.reroot()
		return self.data[key]

	def __contains__(self, key):
		self.reroot()
		return key in self.data

	def update(self, E, **F):
		t = self
		if hasattr(E, 'keys'):
			for k in E.keys():
				t = t.set(k, E[k])
		else:
			for k, v in E.keys():
				t = t.set(k, v)
		for k, v in F.items():
			t = t.set(k, v)
		return t

	def set(self, key, value):
		self.reroot()
		data = self.data
		old_value = data.get(key, NO_VALUE)
		if value is NO_VALUE:
			del data[key]
		else:
			if value is old_value:
				return self
			data[key] = value
		succ = self.successor = PersistentDict()
		succ.data = data
		self.data = {key: old_value}
		return succ

	def delete(self, key):
		return self.set(key, NO_VALUE)

	def keys(self):
		self.reroot()
		return self.data.keys()

	def items(self):
		self.reroot()
		return self.data.items()

	def __repr__(self):
		self.reroot()
		return 'PersistentDict({!r})'.format(self.data)

	def __eq__(self, other):
		if self is other:
			return True
		return set(self.items()) == set(other.items())

	def __ne__(self, other):
		return not self.__eq__(other)