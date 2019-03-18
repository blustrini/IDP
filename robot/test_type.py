
'''
Test not used in final version
'''

a = b'\x01'

print(type(a))

class Class:
	def __init__(self):
		pass

	def test(self):
		return 0

b = Class()

print(type(b.test))


print('y' in str(type(b)))
