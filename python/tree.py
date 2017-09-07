class Node(object):
	def __init__(self, val):
		self.val = val
		self.left = None
		self.right = None

class Tree(object):
	def __init__(self):
		self.root = Node(None)

class BST(Tree):
	def __init__(self):
		super(BST, self).__init__()

	def insert(self, x):
		pass

	def delete(self, x):
		pass

	