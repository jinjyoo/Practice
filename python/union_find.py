class UnionFind(object):  # new-style in Python 2
	'''
	Standard Disjoint-Set structure with union-by-rank and path compression that implements:
	add(x): add an element x to the disjoint-set as its own set, if it's not already in the structure
	find(x): return the representative of the set that x is in
	union(x, y): if x, y are in different sets, then merge the two sets together
	'''


	def __init__(self, lst):
		lst = set(lst)
		self.parents = {i: i for i in lst}  # len(self.parents) to get number of elems
		self.ranks = {i: 0 for i in lst}    # len(self.ranks) to get number of subsets

	def add(self, x):
		if x not in self.parents: 
			self.parents[x] = x

	def find(self, x):  # Path compression
		if x not in self.parents:
			return -1  
		if self.parents[x] != x:  
			self.parents[x] = self.find(self.parents[x])
		return self.parents[x]

	def union(self, x, y):  # Union by Rank
		px, y = self.find(x), self.find(y)
		if px != py:
			r1, r2 = self.ranks[px], self.ranks[py]
			if rx < ry:
				self.parents[px] = py
				del self.ranks[px]
			else:
				if rx == ry:
					self.ranks[px] += 1  # arbitrarily put x as the root
				self.parents[py] = px
				del self.ranks[py]
