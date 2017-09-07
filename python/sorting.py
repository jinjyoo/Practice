"""Resources:
https://en.wikipedia.org/wiki/Sorting_algorithm
http://interactivepython.org/runestone/static/pythonds/index.htm  # Section 5.6
https://www.hackerearth.com/practice/algorithms/sorting/bubble-sort/tutorial/
https://www.tutorialspoint.com/data_structures_algorithms/sorting_algorithms.htm
https://johnderinger.wordpress.com/2012/12/28/quadratic-and-linearithmic-comparison-based-sorting-algorithms/
http://www.geeksforgeeks.org/fundamentals-of-algorithms/#SearchingandSorting
http://www.geeksforgeeks.org/time-complexities-of-all-sorting-algorithms/

https://stackoverflow.com/questions/20761396/why-selection-sort-can-be-stable-or-unstable
"""

import random

a1 = []
a2 = [1]
a3 = [i for i in reversed(xrange(1, 11))]
a4 = [random.randint(-10, 10) for i in xrange(10)]
print a4

# Stable; Not in-place; Not adaptive   # Uses O(n^2) space, see quick_sort2 for improvement
# O(n log n); O(n log n); O(n^2) 
def quick_sort(arr):  
	if len(arr) <= 1:
		return arr  
	pivot = random.choice(arr)  # better than arr[0]
	lesser, equal, greater = [], [], []
	for num in arr:
		if num < pivot:
			lesser.append(num)
		elif num > pivot:
			greater.append(num)
		else:  # equal - includes the pivot itself
			equal.append(num)
	return quick_sort(lesser) + equal + quick_sort(greater)

# Unstable; In-place
# Choosing the pivot: https://stackoverflow.com/questions/164163/quicksort-choosing-the-pivot
def quick_sort2(array, begin, end, version):  #begin/start/left/low;  end/right/high
	# if end is None:
	#     end = len(array) - 1
	if begin < end:   	
		pivot = partition(version)(array, begin, end)	# pivot is in correct position 
		quick_sort2(array, begin, pivot-1, version)    # sort everything before/after the pivot
		quick_sort2(array, pivot+1, end, version)      ##### functools later
	return array  # technically not necessary

def partition(version):  # returns a function
	if version == 0:
		partition_func = partition2
	elif version == 1:
		partition_func = partition3
	elif version == 2:
		partition_func = partition_easy
	elif version == 3:
		partition_func = partition_rand
	return partition_func

def partition2(array, begin, end):  # https://stackoverflow.com/questions/39665299/understanding-quicksort
	pivot = begin   # everything to left of pivot is <= pivot (at start, left of begin is out of bounds, so nothing)
	for i in xrange(begin+1, end+1):  # would have to modify for random
		if array[i] <= array[begin]:  # the pivot value
			pivot += 1
			array[i], array[pivot] = array[pivot], array[i]
	array[pivot], array[begin] = array[begin], array[pivot]
	return pivot

def partition_rand(arr, begin, end):
	pivot = random.randint(begin, end)  # [begin, end]  
	arr[pivot], arr[begin] = arr[begin], arr[pivot]  # put the random element at the start, to be used for true pivot
	return partition2(arr, begin, end)

def partition3(arr, start, end):
	pivot = arr[end]    # sort everything in arr[start:end] on appropriate sides of pivot
	i = start-1   # location of pivot split line; everything ***up to and including*** left of i is <= pivot
	for j in xrange(start, end):   ### note that i < j at all times
		if arr[j] <= pivot:  
			i += 1    # increment since another element will go to left of split line
			arr[i], arr[j] = arr[j], arr[i]
		else: pass    # arr[j] > pivot, which doesn't shift split line (since it's already in correct place: i < j -> right)
	arr[i+1], arr[end] = arr[end], arr[i+1]
	return i+1

# https://stackoverflow.com/questions/39475257/in-place-quicksort-w-last-element-pivot (slight modification of below)
def partition_easy(arr, first, last): # http://interactivepython.org/runestone/static/pythonds/SortSearch/TheQuickSort.html
	pivot = arr[first]
	left, right = first+1, last   
	while left < right:
		while left < right and arr[left] < pivot: # since left is incremented first, it will move past left == right point
			left += 1  
		while right > left and arr[right] >= pivot :  # thus, right stays at the pivot
			right -= 1
		arr[left], arr[right] = arr[right], arr[left]  # two items out of place w.r.t. the eventual split point
	# left > right; everything to left of left <= pivot, and everything to right of right >= pivot
	arr[right], arr[first] = arr[first], arr[right]  # pivot is now in place at index right; arr[first] is correctly placed
	return right   # location of pivot  			



# Stable; Not in-place; Not Adaptive 	# Uses O(n^2) space, use merge2 for improvement (O(n) space)
# O(n log n); O(n log n); O(n log n)	
# See: https://www.quora.com/Algorithms-How-does-merge-sort-have-space-complexity-O-n-for-worst-case
def merge_sort(arr):  	# Top-down implementation   
	if len(arr) <= 1:  	# Base case
		return arr
	# if len(arr) <= 10:  	# Base case
	# 	return insertion_sort2(arr)
	mid = len(arr)//2
	left, right = merge_sort(arr[:mid]), merge_sort(arr[mid:])  
	return merge(left, right)   # tail-recursive, so once done, the space is free

def merge(left, right):
	if not left:
		return right  # could be empty as well
	if not right:
		return left
	if left[0] <= right[0]:  # the equality makes this stable
		return [left[0]] + merge(left[1:], right)  # slicing creates new list; could pass indices instead # No
	else:
		return [right[0]] + merge(left, right[1:])  # Can move to merge_sort to have one method

# https://stackoverflow.com/questions/18761766/mergesort-python
# https://codereview.stackexchange.com/questions/154135/recursive-merge-sort-in-python
def merge2(left, right):   # O(n) space
	l_idx, r_idx = 0, 0
	ret = []
	while l_idx < len(left) and r_idx < len(right):
		if left[l_idx] < right[r_idx]:
			ret.append(left[l_idx])
			l_idx += 1
		else:
			ret.append(right[r_idx])
			r_idx += 1
	ret.extend(left[l_idx:])	# +=
	ret.extend(right[r_idx:]) 
	return ret

# https://stackoverflow.com/questions/2571049/how-to-sort-in-place-using-the-merge-sort-algorithm
def merge_sort3():  # in-place
	pass

# Stable; In-place; Adaptive
# O(n); O(n^2); O(n^2)
# Notes: Sorted array starts from right
def bubble_sort(arr):
	bound = len(arr)-1  # everything past bound's index has been sorted  # handles 0-1 case automatically
	not_sorted = True
	while not_sorted and bound > 0:  
		not_sorted = False
		for i in xrange(bound):  	# last i is the second-to-last element
			if arr[i] > arr[i+1]:  	# no ==, so stable
				not_sorted = True
				arr[i], arr[i+1] = arr[i+1], arr[i]		
		bound -= 1  # the largest element has bubbled up to the top
	return arr 		# since in-place, technically don't need to return

def bubble_sort2(arr):   # 11 lines instead of 13
	not_sorted = True
	for bound in xrange(len(arr)-1, 0, -1):
		if not not_sorted:
			break
		not_sorted = False
		for i in xrange(bound):  
			if arr[i] > arr[i+1]:
				not_sorted = True
				arr[i], arr[i+1] = arr[i+1], arr[i]
	return arr

# Not stable; In-place; Not adaptive
# O(n^2), O(n^2), O(n^2)  
# Notes: Can have its sorted subarray grow from the left or right (getting min vs max)
def selection_sort(arr):
	for start in xrange(len(arr)-1):  # growing from left   # handles 0-1 case; added -1 to ignore last elem (already correct)
		idx = start  	# idx is index of curr_min; initialize to start of unsorted subarray
		for i in xrange(start+1, len(arr)):
			if arr[i] < arr[idx]:   
				idx = i
		arr[start], arr[idx] = arr[idx], arr[start]	 # Unstable, e.g. [3, 3, 1]; can make stable by inserting at start   
	return arr

# Stable; In-place; Adaptive
# O(n); O(n^2); O(n^2)
# 
def insertion_sort(arr):  # Conceptually clearer, but less efficient than insertion_sort2
	for start in xrange(1, len(arr)):  # start of unsorted
		idx = start  
		while idx > 0 and arr[idx-1] > arr[idx]:
			arr[idx], arr[idx-1] = arr[idx-1], arr[idx]
			idx -= 1
	return arr

# Straight-Insertion-Sort: Instead of swapping every time, we swap once we find the insert location
def insertion_sort2(arr):  # http://codereview.stackexchange.com/questions/139056/insertion-sort-in-python
	for start in xrange(1, len(arr)):
		idx, val = start, arr[start]  # save val
		while idx > 0 and arr[idx-1] > val:
			arr[idx] = arr[idx-1]
			idx -= 1
		arr[idx] = val   # pointless if idx didn't increment
	return arr


"""################### OTHER SORTS ###################"""

# Not stable; In-place; Adaptive  ### See counting_sort2
# O(n), O(n), O(n); O(n+k) space    ### Note, if bound is not given then O(n+k) where k is the maximum (need to find)
# Note: Only works if you know the range of numbers   # Not a comparison-based sort  # Can be extended to negative numbers
# https://stackoverflow.com/questions/32342387/is-using-a-hash-table-valid-in-counting-sort-in-place-of-an-array
def counting_sort(arr, bound):  # Assume lower bound is 0   
	if len(arr) <= 1:  # for speed
		return arr
	# bound = max(arr) 
	# count = Counter(arr)  # can't use since unordered
	counter = [0]*(bound+1)
	for num in arr:
		counter[num] += 1
	ret = []   ### ALTERNATIVELY, can just overwrite arr
	for num in xrange(len(counter)):
		if num:
			ret.extend([num]*counter[num])
			# arr[prev : prev + counter[num]] = [num]*counter[num]
	return ret

# Note: Counting sort can be extended to non-integers by hashing (assigning numbers to values)
def counting_sort2(arr, bound=256):  # stable version   # assume strings, in which case ASCII
	if len(arr) <= 1:
		return arr
	counter = [0]*(bound)
	for x in arr:   			# not "num" 
		counter[ord(x)] += 1    # key(i) in general
	for i in xrange(1, len(counter)):
		counter[i] += counter[i-1]     # cumulative sum - counter[i] stores the number of items with keys less than i
	output = [0]*(bound+1)  
	for x in arr:	# counter[i] stores the next position in the output array into which an item with key i would be stored
		key = ord(x)
		output[counter[key]] = x
		counter[key] -= 1
	return output
		
def radix_sort(arr):    # negatives?
	if len(arr) <= 1:
		return arr
	counter = []*10  # digits 0-9; finite range, so good for counting sort

def counting_sort3(arr, exp):
	pass

def shell_sort(arr):
	if len(arr) <= 1:
		return arr
	gap = len(arr)//2
	while gap > 0:
		for i in xrange(0, len(arr)-gap-1, gap):
			temp = arr[i]
			j = i
			# if arr[i] > arr[i + gap]:   # Changed - same optimization as in Insertion Sort
			# 	arr[i], arr[i + gap] = arr[i + gap], arr[i]


def bucket_sort(arr):  
	if len(arr) <= 1:
		return arr

# Stable; Not in-place; Adaptive
# O(n); O(n log n); O(n log n)
# Mix of merge + insertion; standard sorting used by Python
def tim_sort(arr):  # https://en.wikipedia.org/wiki/Timsort
	if len(arr) <= 63:
		return insertion_sort(arr)

def heapsort(arr):  
	if len(arr) <= 1:
		return arr

		