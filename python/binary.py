"""Handling cases:
https://stackoverflow.com/a/30928332
https://stackoverflow.com/a/39227182
https://stackoverflow.com/a/35257092
"""
#Exclusive bound: don't increment (applies to both low/high)
#Inclusive bound: increment 
"""Very important: make sure low/high you're always moving.  Analysis of loop invariants, see:
https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/description/ 
And rigorously proving: 
https://discuss.leetcode.com/topic/6112/a-concise-solution-with-proof-in-the-comment/5

Analysis on binary search problems in general:
https://discuss.leetcode.com/topic/52948/share-my-thoughts-and-clean-java-code
https://discuss.leetcode.com/topic/52865/my-solution-using-binary-search-in-c/32?page=2
"""



a = range(10)
b = [1, 2, 3, 5]  # check for 0, 4, 6

def search1(key, arr=a):        # preferred   [low, high) 
	low, high = 0, len(arr)     # easier to think about it when len(arr) == 0
	while low < high:           # at end of loop, low == high, so don't have to worry about which to use 
		mid = low + (high-low)/2  # bias is too low, so need extra movement from the low side, can't use low = mid
		if arr[mid] < key:      # mid is not in the feasible bound
			low = mid+1         # we want _low_ to be in the feasible bound, so move past mid
		elif arr[mid] > key:
			high = mid          # we don't want high in the bound, so set high to mid (which we know isn't in bound)
		else:						### High is never mid (round down, and low < high), so interval always shrinks
			return mid          # if not checking mid in while, then return low; mid biases to low and high is exclusive bound
	return -1  					### If doing "forgetful" (without == check), then return low since high is not in sol. space

# If your bounds are inclusive, then when low = high there's one element left in the array to check and 
# the inner loop should run another time. Therefore, a test of whether low <= high is appropriate.
def search2(key, arr=a):   #[low, high]
	low, high = 0, len(arr)-1
	while low <= high:          # both left/right are included, need <= for narrowed to one element available (low == high)
		mid = low + (high-low)/2
		if arr[mid] < key:
			low = mid+1
		elif arr[mid] > key:
			high = mid-1
		else:
			return mid
	return -1

def search3(key, arr=a):  #(low, high)
	low, high = -1, len(arr) # if high = 0, then while-loop doesn't run
	while (high - low) > 1:  # at least one element between low and high (e.g. (1, 3) -> 2)
		mid = low + (high-low)/2
		if arr[mid] < key:
			low = mid
		elif arr[mid] > key:
			high = mid
		else:
			return mid
	return -1
#######################################################################
#Alternate: https://stackoverflow.com/a/24349252  ("Forgetful binary")
"""Use forgetful binary when the equality check is implicit or unknown (can't be applied directly)"""
"""Note: "low < high", and the change in low/mid incrementing; see search6 for details"""
"""Basically, if you do checks in the loop itself, you exit when 0 elements are left to be candidates;
otherwise, you exit with one element left to be inspected."""
def search4(key, arr=a):
	low, high = 0, len(arr)-1  #[low, high]   # preferred for forgetful
	while low < high:   # not the usual <=; in non-forgetful, if low == high then there's one element left to be checked,
						# which happens in the while-loop itself. Here, there's no separate == check, so we exit when there's
						# only one element left (low < high implies low != high, and low/high are both in bound so >1 element)
						# and then check if low is the answer then.
		mid = low + (high-low)/2  # Bias is low, so need extra movement from the low side, can't use low = mid
		if arr[mid] < key:
			low = mid + 1
		else:
			high = mid   # not the usual mid-1; on equality, high moves down
						 ### because we don't have separate == check, this could trigger if arr[mid] = key,
						 # and since high IS included in the viable range, we set high = mid instead of excluding w/ mid-1
	return low # if arr[low] == key else -1    # low == high so can return high, too
	### ALTERNATIVELY: can return "low" instead of -1 if you want the index that "key" would've been at if it had existed
		#However, if it would be bigger than the biggest element then it'll cap at len(arr)-1 instead of returning len(arr)...
		# How to fix?  Ideally we want the index of the first element greater than the key, 
		 #or a.length if all elements in the array are less than the specified key.

"""Note: Search 5 fails if key not found, because low does not move; so don't use it"""
def search5(key, arr=a):
	low, high = 0, len(arr)-1
	while low < high:
		mid = low + (high-low)/2
		if arr[mid] <= key:   # now, the equality check is with low
			low = mid     # can't move past mid since it might be the answer   ### BAD
		else:
			high = mid-1  # inclusive
	return low # if arr[low] == key else -1 # we exit if low == high; both low and high are valid, so this makes sense

def search6(key, arr=a):
	low, high = 0, len(arr) # [low, high)
	while (high - low) > 1: # If we exit, that implies low+1 = high; high is excluded, so low is the only candidate,
							# and since we don't check the key in the while-loop, we exit the loop and check outside
							# Cf: low < high (non-forgetful). We exit when low == high, but low is inclusive while high
							# is exclusive, which doesn't make sense; we don't return low here, but instead, we should
							# have already found the result in the while-loop itself (which handled the final iteration
							# low + 1 = high, where 'low' was the final candidate before low would reach high (exclusive))
		mid = low + (high-low)/2
		if arr[mid] <= key:
			low = mid  # don't need low to move?  # not the usual mid+1, since low might be the final return
		else:
			high = mid # exclusive; the reason for not moving is different from low not moving
	return low   # we exit once low = high+1; since high is exclusive, we return low

# def search6(key, arr=a):
# 	low, high = 0, len(arr)
# 	while (high - low) > 1:
# 		mid = low + (high-low)/2
# 		if arr[mid] < key:
# 			low = mid+1
# 		else:


# For all these searches, can bias towards high, in which case need to make sure high is moving properly instead of low
def bias_high(key, arr=a):
	low, high = 0, len(arr)-1
	while low < high:  
		mid = low + (high-low+1)/2 # bias towards high
		if arr[mid] > key:
			high = mid-1
		else:
			low = mid   # not the usual mid+1
	return low if arr[low] == key else -1   
	# return low+1  # can't do high, have to do high+1


# if __name__ == "__main__":
# 	while True:
# 		key = map(int, raw_input().strip().split(' '))
# 		print 'Index is: {0}'.format(search(key))

def check(arr, key):
	i, j = 0, len(arr)
	while i < j:
		m = (i + j) / 2
		if arr[m] < key:
			i = m + 1
		else:
			j = m
	print i, m, j

def lengthOfLIS(self, nums):
    tails = [0] * len(nums)
    current_max = 0
    for x in nums:
        i, j = 0, current_max
        while i < j:
            m = (i + j) / 2
            if tails[m] < x:
                i = m + 1
            else:
                j = m
        tails[i] = x
        current_max = max(i + 1, current_max)
        print x, i, tails
    return current_max

"""Examples of searching without knowing the key - need forgetful version
# https://leetcode.com/problems/kth-smallest-element-in-a-sorted-matrix/description/
# https://leetcode.com/problems/find-the-duplicate-number/description/
https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/description/ # Note checks in both in and out of loop
"""
        import heapq
        # import itertools
        # next(itertools.islice(heapq.merge(*matrix), k-1, k))   # Won't work since we don't have a specific index