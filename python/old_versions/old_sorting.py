import random

a1 = []
a2 = [1]
a3 = [i for i in reversed(xrange(1, 11))]
a4 = [random.randint(-10, 10) for i in xrange(20)]
print a4

### Merge/Quick: Preserves original list (due to slicing).  Bubble/Selection/Insertion: modifies original list

def merge_sort(arr):
	if len(arr) <= 1:  # if not arr
		return arr
	# if len(arr) < 10: return insertion_sort(arr)
	mid = len(arr) // 2
	left, right = merge_sort(arr[:mid]), merge_sort(arr[mid:])
	return merge(left, right)
	# return merge(arr[:mid], arr[mid:])

def merge(left, right):  # expects left and right to already be sorted
	if not left:
		return right
	if not right:
		return left
	if left[0] < right[0]:
		return [left[0]] + merge(left[1:], right)
	else:
		return [right[0]] + merge(left, right[1:])

def quick_sort(arr):
	if len(arr) <= 1:
		return arr
	# if len(arr) < 10: return insertion_sort(arr)
	lesser, equal, greater = [], [], []
	pivot = arr[0]
	for elem in arr:
		if elem < pivot: 
			lesser.append(elem)  # faster for singles; can result in infinite recursion (use 'extend'); += creates new list
		elif elem > pivot:
			greater.append(elem)
		else:
			equal.append(elem)
	return quick_sort(lesser) + equal + quick_sort(greater)

def insertion_sort(arr):
	for i in xrange(1, len(arr)):
		j = i
		while j > 0 and arr[j] < arr[j-1]:
			arr[j], arr[j-1] = arr[j-1], arr[j]
			j -= 1  # j = j-1
	return arr

def insertionSort(lst):  # http://codereview.stackexchange.com/questions/139056/insertion-sort-in-python
    for index in xrange(1, len(lst)):
        currentvalue = lst[index]
        position = index
        while position > 0 and lst[position - 1] > currentvalue:
            lst[position] = lst[position - 1]
            position -= 1
        lst[position] = currentvalue

def bubble_sort(arr):  
	not_sorted = True 
	num_passes = 0
	while not_sorted:
		not_sorted = False  # ugly
		i = 0
		while i < len(arr)-1-num_passes:
			if arr[i] > arr[i+1]:
				not_sorted = True
				arr[i], arr[i+1] = arr[i+1], arr[i]  # swap
				i += 1
			i += 1
	return arr
	# for i in xrange(len(arr)-1):
	# 	if arr[i] > arr[i+1]:
	# 		arr[i], arr[i+1] = arr[i+1], arr[i]  # swap

def selection_sort(arr):  # can either find max and build from right, or min and build from left
	cursor = 0
	for i in xrange(len(arr)):
		smallest_index = cursor  # or i
		for j in xrange(cursor, len(arr)):
			if arr[j] < arr[smallest_index]:
				smallest_index = j
		arr[smallest_index], arr[cursor] = arr[cursor], arr[smallest_index]
		cursor += 1

	# while cursor < len(arr):
	# 	smallest_index = cursor  # moved
	# 	for i in xrange(cursor, len(arr)):  # redefined here, so does work (cf: above)
	# 		if arr[i] < arr[smallest_index]:
	# 			smallest_index = i
	# 	arr[smallest_index], arr[cursor] = arr[cursor], arr[smallest_index]
	# 	cursor += 1
	# return arr

def first_character(str): # first character that appears once in string
	ret = ''

def increasing_subsequence(str):
	pass
	# let this be done later



	# if not left: return right  # why "not"? Check Mark Miyashita

from collections import deque



def bfs1(graph, start):
    visited, queue = set(), [start]
    while queue:
        vertex = queue.pop(0)
        if vertex not in visited:
            visited.add(vertex)
            queue.extend(graph[vertex] - visited)
    return visited

def dfs1(graph, start):
    visited, stack = set(), [start]
    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            visited.add(vertex)
            stack.extend(graph[vertex] - visited)
    return visited

def bfs(graph, start):
	visited, frontier = [], deque([start])
	while frontier:
		node = frontier.popleft()
		if node not in visited:
			for neighbor in graph[node]:
				if neighbor not in visited:
					frontier.append(neighbor)
			visited.append(node)
	return visited

def dfs(graph, start):
	visited, frontier = [], deque([start])  # use as a stack
	# for node in frontier:  # this will freeze things
	while frontier: 
		node = frontier.pop()
		if node not in visited:
			for neighbor in graph[node]:
				if neighbor not in visited: 
					frontier.append(neighbor)
			visited.append(node)
	return visited

graph = {'A': ['C', 'B'],
         'B': ['A', 'D', 'E'],
         'C': ['A', 'F'],
         'D': ['B'],
         'E': ['B', 'F'],
         'F': ['C', 'E']}	

# graph = {'A': set(['C', 'B']),
#          'B': set(['A', 'D', 'E']),
#          'C': set(['A', 'F']),
#          'D': set(['B']),
#          'E': set(['B', 'F']),
#          'F': set(['C', 'E'])}	

class Solution(object):
    def isValidBST(self, root):
        """
        :type root: TreeNode
        :rtype: bool
        """
        return self.isValidBst(root,-2147483649,2147483648)
        
        
    def isValidBst(self,root,minVal,maxVal):
        if not root :
            return True
        if root.val >=maxVal or root.val <=minVal:
            return False
        return self.isValidBst(root.left,minVal,root.val) and self.isValidBst(root.right,root.val,maxVal)
     

    private void inorder(TreeNode root) {
        if (root == null) return;
        inorder(root.left);
        handleValue(root.val);
        inorder(root.right);
    }