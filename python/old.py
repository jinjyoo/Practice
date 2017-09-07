class Heap: 

	def __init__(self, arr=None): # binding the default argument at function definition, and not at function execution
		if arr is None: arr = []
		self.heap = arr  # self.heap = (arr if arr is not None else [])

	def insert(self, x):
		self.heap.append(x)
		pos_x = len(self.heap)-1  
		parent_x = self.parent(pos_x)
		while pos_x > 0 and self.heap[pos_x] < self.heap[parent_x]:  
			self.heap[pos_x], self.heap[parent_x] = self.heap[parent_x], self.heap[pos_x]
			pos_x, parent_x = parent_x, self.parent(parent_x)

	def delete(self):  
		if not self.heap:
			return "Heap is empty."
		if len(self.heap) > 1:
			self.heap[0], self.heap[-1] = self.heap[-1], self.heap[0]
			ret = self.heap.pop()  # old root is gone
			pos_x = 0
			child_x = self.best_child(pos_x)  # index
			while child_x and self.heap[pos_x] > self.heap[child_x]:  # pos_x is wrong, changed to child_x
				self.heap[pos_x], self.heap[child_x] = self.heap[child_x], self.heap[pos_x]
				pos_x, child_x = child_x, self.best_child(child_x)
			return ret

	def decrease_key(self, index, new_value):
		pass  #TODO

	def heapsort():
		pass  #TODO

	def get_root(self):
		if self.heap: return self.heap[0]

	def _siftup(self, x):
		pass

	def _siftdown(self, x):
		pass

	def parent(self, i):
		return (i-1)/2 if i > 0 else None

	def left(self, i):
		l_x = 2*i+1
		return l_x if l_x < len(self.heap) else None

	def right(self, i):
		r_x = 2*i+2
		return r_x if r_x < len(self.heap) else None

	def best_child(self, i):
		l_x, r_x = self.left(i), self.right(i)                      	# filter(None) removes 0 too but never should be 0
		# return max(self.heap[i] for i in filter(None, (l_x, r_x)))  	# note: don't need [] since wrapped in function
		if r_x:  # there must be a left									# max(None, None) = None
			left, right = self.heap[l_x], self.heap[r_x]
			return l_x if left < right else r_x
		elif l_x: return l_x 
		else: return None

h = Heap()
for i in xrange(9, 0, -1): 
	h.insert(i)
	print h.heap

	# def __repr__(self):
	# 	pass
	# 	# http://wisercoder.com/heap-implementation-python/

def heapify(arr, n, i):  # n = (arr)
	pass
	# parent = arr[0]
	# c1, c2 = 

def heapsort():
	pass
