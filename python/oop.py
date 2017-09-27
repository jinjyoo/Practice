# https://www.reddit.com/r/learnpython/comments/3q077n/global_vs_nonlocal/

x = 100

class Test(object):  # For Python2 compatibility

	class Nested(object):  # n = Test.Nested()

		x = -5

		def __init__(self): 
			self.x = -1

		def foo(self):
			global x
			print(x)
			# nonlocal x  # name x is nonlocal and global
			# print(x)
			# global y    # global y (and _y) is not defined; does not see _y  
			# print(y)


	x = 1   # Test.x
	_y = 'a'  # still imported, since we have to access with Test.y or t.y anyway.  Only global level is affected.
	_k = 'final'
	__z = 'b'

	def __init__(self):   # t.x
		self.x = 2
		# print(y)   # y is not defined
		print(self.y)  # prints 'a'

	@property
	def k(self):  # https://stackoverflow.com/questions/802578/final-keyword-equivalent-for-variables-in-python
		return self._k

	@k.setter  # without a property, will error: name 'k' not defined
	def k(self, char):
		print("get out")
		return  
		"""No longer necessary"""
		if hasattr(self, 'k'):  # also works with '_k'   # technically don't need this
			print("Should not be modifying")

	@property  # getter
	def y(self):      #t.y; but can still access with t._y
		print('Tingling')
		# return self.y   # Infinite recursion of printing
		return self._y

	@y.setter
	def y(self, char):
		if self.y == 'a':    # only allow modifications from that   ### not working
			self._y = char   # all of these self.y and self._y's are interchangeable for now, .y is slightly slower
		else:				 # ^Edit: no longer interchangeable, since we modified y.getter to print 
			print("Only one change allowed.")

	@y.deleter
	def y(self):
		del self._y  # remove variable y;  # deleting does not print 'Tingling'

	def foo(self):
		# x = 5   # name 'x' is assigned before global declaration 
		global x
		x = 3   # printing module's x will now return 3
		print(x)   # prints 3
		def bar():
			# nonlocal x    # no binding for x found -> ignores previous x because that's global
			x = 4
			print(x)  # prints 4
			def foobar():
				x = 1
				print(x)  # prints 1
				def tiny():
					nonlocal x
					x = -5
					print(x)   # prints -5
				print(x)  # still prints 1, because tiny hasn't been called yet
				return tiny
			return foobar
		return bar

	def a():  # self is not explicitly used, so static method (no error even without decorator); call with Test.a()
		x = 'a()'
		def b():
			# x = 'b()'   
			def c():
				# nonlocal x  # this isn't even necessary since we just print, aren't modifying -> closure
				print(x) # prints b()  -> prints 'a()' without b, since it goes up
			c()
		b()
	
	def f():
		total = 0
		def g(x):
			print(total)  # local variable 'total' referenced before assignment   # prints 0 if next two lines are removed
			total += x    # local variable 'total' referenced before assignment
			print(total)
		return g


	@staticmethod
	def msg():
		print("Hi")

	@classmethod
	def peek(cls):   # this can be called with t.peek() as well as Test.peek()
		print("You are in {0}".format(cls.__name__))

	def check_nested(self):
		n = Nested()
		print(self.x == n.x)
		global x  # since we don't have access to cls
		print(x == Nested.x)

	def check_neighbor(self):
		neighbor = Test2()
		print(Test2().msg)
		try:
			print(Test2()._hidden)
		except NameError:
			print("Private variable can't be accessed")

_actually_hidden = 'Boing'  # 'will error since not found'
__fake_hidden = 'Ding-Dong'  # no mangling, only invoked if it's a class variable -> _<class>__fake_hidden
							 #! However, it still starts with '_', so it is not imported

class Test2(object):
	msg = 'Hi'
	_hidden = 'Hola'    # only hides from imports?  ### todo
	__mangled = 'Salut' # can reference in Test3 with Test3()._Test2__mangled
 
	def _hiding():
		print('yo')

	def hmm():
		_x = 'boo!'
		print(_x)

class Test3(Test2):

	def __init__(self):
		# super(Test3, self).__init__()  # Python2
		super().__init__()  
		print(self._hidden)  # prints just fine even if imported

# if __name__ == '__main__':
# 	t = Test() 
# 	print t.x
# 	print t.Test()