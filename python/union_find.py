# See also: https://github.com/israelst/Algorithms-Book--Python/blob/master/5-Greedy-algorithms/kruskal.py

class UnionFind(object):  # new-style in Python 2
	'''
	Standard Disjoint-Set structure with union-by-rank and path compression that implements:
	add(x): add an element x to the disjoint-set as its own set, if it's not already in the structure
	find(x): return the representative of the set that x is in
	union(x, y): if x, y are in different sets, then merge the two sets together
	'''

	def __init__(self):
        self.parents = {}  # len(self.parents) to get number of elems
        self.ranks = {}    # len(self.ranks) to get number of subsets  
    
    def add(self, x):
        if x not in self.parents:
            self.parents[x] = x
            self.ranks[x] = 0
            
	def find(self, x):  # Path compression - make sure every node directly points to the representative
		if x not in self.parents:
			return None
        if self.parents[x] != x:
            self.parents[x] = self.find(self.parents[x])
        return self.parents[x]  # should be the representative

    def find(self, x):
        if self.parents[x] != x:
            self.parents[x] = self.find(self.parents[x])
        return self.parents[x]  # should be the representative
    
    def union(self, x, y):
		px, py = self.find(x), self.find(y)   # use find() to initiate path compression
        if px != py:
            rx, ry = self.ranks[x], self.ranks[y]
            if rx < ry:
				self.parents[px] = py
				del self.ranks[px]    # safe to delete, since if union(x, y) is called again, we won't enter this loop
			else:
				self.parents[py] = px
				del self.ranks[py]
				if rx == ry:
					self.ranks[px] += 1  # arbitrarily put x as the root
                   
def kruskal(vertices, edges):
    uf = UnionFind()
    for vertex in vertices:
        uf.add(vertex)
    mst = set()
    edges.sort()
    # TODO
        