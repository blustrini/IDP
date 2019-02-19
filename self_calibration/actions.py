class Actions():
	def __init__(self):
		self.actions = {}

	def assemble_func(self,choice):
		list = []
		for i in choice:
			list.append(self.actions[i])
		return list

