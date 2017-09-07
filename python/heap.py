# from operator import le, ge

"""
Links:
https://en.wikipedia.org/wiki/Heap_(data_structure)#Operations
https://en.wikipedia.org/wiki/Binary_heap#Heap_operations 
https://courses.cs.washington.edu/courses/cse373/11wi/homework/5/BinaryHeap.java

Heapify and HeapSort:
https://www.hackerearth.com/practice/notes/heaps-and-priority-queues/
http://www.geeksforgeeks.org/heap-sort/
http://www.personal.kent.edu/~rmuhamma/Algorithms/MyAlgorithms/Sorting/heapSort.htm
http://www.cs.toronto.edu/~krueger/cscB63h/w07/lectures/tut02.txt
"""

"""Interesting problems
https://leetcode.com/problems/kth-smallest-element-in-a-sorted-matrix/description/
https://leetcode.com/problems/search-a-2d-matrix-ii/description/
"""

class Heap(object):

	def __init__(self, arr=None):
		self.heap = arr if arr else []  # binding the default argument at function definition, and not at function execution
		# self.heap = arr if arr is not None else [] 
		# self.f = le if is_min else ge

	def __len__(self):
		return len(self.heap)

	def __str__(self):
		return str(self.heap)

	def sift_up(self, idx):  # restore heap condition 
		pid = self.p_idx(idx)
		try:  # don't abuse try, minimize code to avoid masking errors
			while self.heap[idx] < self.heap[pid]:
				self.heap[idx], self.heap[pid] = self.heap[pid], self.heap[idx]  # swap child with parent
				idx, pid = pid, self.p_idx(pid)
		except TypeError:  # pid is None
			pass
		
	def sift_up_recursive(self, idx):
		pid = self.p_idx(idx)
		if pid is not None and self.heap[idx] < self.heap[pid]:  # if
			self.heap[idx], self.heap[pid] = self.heap[pid], self.heap[idx]  # swap 
			self.sift_up_recursive(pid)  # Only recurse if we sifted

	def sift_down(self, idx):
		cid = self.c_idx(idx)
		while cid is not None and self.heap[idx] > self.heap[cid]:  
			self.heap[idx], self.heap[cid] = self.heap[cid], self.heap[idx]
			idx, cid = cid, self.c_idx(idx)

	def decrease_key(self, idx, new_val):  # for min_heap
		self.heap[idx] = new_val
		self.sift_up(idx)

	def change_key(self, idx, new_val):   # changing priority   
		old_val, self.heap[idx] = self.heap[idx], new_val
		if new_val > old_val:
			self.sift_down(idx)
		elif new_val < old_val:
			self.sift_up(idx)

	def insert(self, num):
		self.heap.append(num)
		self.sift_up(len(self)-1)

	def delete(self, idx):  # deletes and returns self.heap[idx] (arbitrary index)
		if idx > len(self)-1:
			print "{0} is not in range of heap.".format(idx)
			return 
		self.heap[idx], self.heap[-1] = self.heap[-1], self.heap[idx]
		ret = self.heap.pop()  
		self.sift_down(idx)  # idx now holds what used to be one of the biggest values, need to sift down
		return ret

	def extract_min(self):
		return self.delete(0)

	def find_min(self):
		return self.heap[0]

	def p_idx(self, cid):
		return (cid-1)/2 if cid > 0 else None

	def l_idx(self, pid):
		left = 2*pid+1
		return left if left < len(self.heap) else None  #left is never 0 so safe to use "if left"

	def r_idx(self, pid):
		right = 2*pid+2
		return right if right < len(self.heap) else None

	def c_idx(self, pid):
		cid = left = self.l_idx(pid)
		if left:
			right = self.r_idx(pid)
			if right and self.heap[right] < self.heap[left]:
				cid = right
		return cid  # could be None

	@staticmethod  
	def max_heapify(arr, idx, n):  # Complexity: O(h) = O(log n)  
		# cid = Heap.c_idx1(idx)  # Can't do, unfortunately
		left, right = 2*idx+1, 2*idx+2
		left = left if left < n else None
		right = right if right < n else None
		cid = right if right and arr[right] > arr[left] else left  # cid could be None
		largest = cid if cid and arr[cid] > arr[idx] else idx  # can't do idx since we're checking cid != None
		if largest != idx:   # was not already a heap
		# if cid and arr[cid] > arr[idx]:    # more concise, but less clear
			arr[idx], arr[cid] = arr[cid], arr[idx]   # now the subtree at idx is a heap, with largest element at idx (root)
			Heap.max_heapify(arr, largest, n)   # only need to go down one child, since it's bigger than idx and other_child
			# ^ It is important to note that swap may destroy the heap property of the subtree rooted at the largest child node. 
			#   If this is the case, Heapify calls itself again using largest child node as the new root.

	"""Elements from Arr[(n-1)/2] to arr[n-1] are leaf nodes,and each node is a 1 element heap. Thus we only need process 
	the non-leaf nodes, from N/2 to 1 (bottom up, so not 1 to N/2)"""
	# O(n): See http://www.cs.umd.edu/~meesh/351/mount/lectures/lect14-heapsort-analysis-part.pdf
	@staticmethod  # Note: works on min_heap, too, so functions as min_to_max
	def build_max_heap(arr):  #O(n), faster than the O(n log n) of doing insert() on every element
		"""The bottom-up order of processing node guarantees that the subtree rooted at children are heap 
		before 'Heapify' is run at their parent.  However, max_heapify itself works from the top downward (sift_down)"""
		n = len(arr)  # constant in this case, but need for heapsort
		"""unlike in heapsort(), we include the root"""
		for i in xrange((len(arr)-2)/2, -1, -1):      # bottom-up  	# starting from parent of last leaf; see p_idx
			Heap.max_heapify(arr, i, n)     		  # top-down   	# technically, only up to 2*i+2 is considered, not n
																	# so "l/r < n" check is inefficient for this part
	@staticmethod
	def heapsort(arr): # O(n log n): dominated by for-loop which runs O(n) times and heapify takes O(log n)
		n = len(arr)
		Heap.build_max_heap(arr)
		for i in xrange(len(arr)-1, 0, -1):  # don't need to include root (arr[0]) since that should be smallest element
			arr[i], arr[0] = arr[0], arr[i]
			Heap.max_heapify(arr, 0, i)      # effective heap is up to i; everything past i has been sorted, so ignore
		return arr 							 # top-down, since max_heap
# h = Heap()
# for i in xrange(9, 0, -1): 
# 	h.insert(i)

class FiboHeap(Heap):
	pass



