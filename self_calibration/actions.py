class Actions():
	def __init__(self,Master,dict):
		#master task in housed in Master object
		self.Master = Master
		self.actions = dict


	def assemble_func(self,data):
		#create function
		list = []
		for i in data[0]:
			list.append(self.actions[i])

		#set state
		self.Master.state = data[1]
		
		#return list
		return list


'''
Resetting the state every trigger might be wasiting time
'''
