"""
https://leetcode.com/problems/sum-of-left-leaves/description/
"""

class Node(object):
	def __init__(self, val):
		self.val = val
		self.left = None
		self.right = None

class Tree(object):
	def __init__(self, val):
		self.root = Node(val)

	"""Standard helper methods"""
	def height(node):
		if not node: return 0
		return 1 + height(node.left) + height(node.right)

	def num_children(node):
		if not node: return 0
		left = 0 if not node.left else 1 + num_children(node.left)  # base case implied
		right = 0 if not node.right else 1 + num_children(node.right)
		return left + right

	def diameter(root):
		self.diameter = 0  # can avoid global variable by using something like: diameter = [0]; helper(root, diameter)
		helper_diameter_cleaner(root)
		return self.diameter

	def helper_diameter(node): # https://leetcode.com/problems/diameter-of-binary-tree/description/
		if not node: return 0
		left = 0 if not node.left else 1 + helper_diameter(node.left)  # postorder; like num_children
		right = 0 if not node.right else 1 + helper_diameter(node.right)
		self.diameter = max(self.diameter, left + right)
		return max(left, right)  # note the triple calculations of path (left + right), diameter, and max(l, r)

	def helper_diameter_cleaner(node):  # cleaner but slightly harder to understand than helper_diameter
		if not node: return 0
		left = helper_diameter_cleaner(node.left)
		right = helper_diameter_cleaner(node.right)
		self.diameter = max(self.diameter, left + right)
		return max(left, right) + 1

class BST(Tree):
	def __init__(self):
		super(BST, self).__init__()

	def insert(self, x):
		pass

	def delete(self, x):
		pass

