"""
Need to finish SegmentTreeHeap:
    https://stackoverflow.com/questions/41085553/segment-tree-implementation-in-python
    https://leetcode.com/articles/recursive-approach-segment-trees-range-sum-queries-lazy-propagation/
    https://leetcode.com/articles/range-sum-query-mutable/#approach-3-segment-tree-accepted

BIT: https://discuss.leetcode.com/topic/31599/java-using-binary-indexed-tree-with-clear-explanation
**https://cs.stackexchange.com/questions/10538/bit-what-is-the-intuition-behind-a-binary-indexed-tree-and-how-was-it-thought-a
"""

import unittest

# http://www.geeksforgeeks.org/segment-tree-set-1-sum-of-given-range/
class SegmentTreeHeap(object):
    """All levels will be filled except possibly bottom level.  N leaves.
    Full Binary Tree, since we always divide segments into 2 (or not at all).
    Full + N leaves --> 2n-1 nodes, which is length of our array
    For index i, children at 2*i+1, 2*i+2 (0-indexing); parent at floor((i-1)/2)
    """
    def __init__(self, arr):
        if not arr:
            self.tree = None
        self.tree = [0]*(2*len(arr)-1)   # Less space, but slower since we'd have to do null checks
        # self.tree = [0]*(2*len(arr))

    def build(self, arr, idx, left, right):
        if left == right:
            self.tree[idx] = arr[left]
            return
        mid = (left + right)/2
        self.build(arr, 2*idx+1, left, mid)
        self.build(arr, 2*idx+2, mid+1, right)
        self.tree[idx] = self.tree[2*idx+1] + self.tree[2*idx+2]  
        # self.tree[idx] = self.merge(arr, 2*idx+1, 2*idx+2)   # general: could be min, max, etc.
    
    # def query(self, qi, qj, idx=0, left=0, right=n-1):  
    def query(self, idx, left, right, qi, qj):
        if left > qj or right < qi:     # segment completely outside range
            return 0
        if qi <= left and qj >= right:  # segment completely inside range
            return self.tree[idx]
        mid = (left + right)/2  # partial overlap of current segment and queried range. Recurse deeper.
        return self.query(2*idx+1, left, mid, qi, mid) + self.query(2*idx+2, mid+1, right, mid+1, right)

        """slight pruning + generic merge"""
        if i > mid:
            return self.query(2*idx+2, mid+1, right, mid+1, right)
        elif j <= mid:
            return self.query(2*idx+1, left, mid, qi, mid)
        left_query = self.query(2*idx+1, left, mid, qi, mid)
        right_query = self.query(2*idx+2, mid+1, right, mid+1, right)
        return self.merge(left_query, right_query)

    def update(self, curr, left, right, idx, new_val):
        if left == right:  # leaf node, update element
            self.tree[left] = new_val
            return
        mid = (left + right)/2 
        if idx <= mid:
            self.update(2*curr+1, left, mid, idx, new_val)
        else:  # idx > mid:
            self.update(2*curr+2, mid+1, right, idx, new_val)
        self.tree[idx] = self.tree[2*curr+1] + self.tree[2*curr+2]  # one was updated
        # self.tree[idx] = self.merge()  
    

"""Original implementation - Tree"""
class Node(object):
    def __init__(self, span):
        self.span = span  # tuple indicating range
        self.val = None
        self.left = None
        self.right = None  

class SegmentTree(object):
    def __init__(self, arr):  # is left-heavy; [0-5] splits into [0, 1], [2, 2] ; [3, 4], None
        n = len(arr)
        self.arr = arr   # just for diff logic; otherwise we could just use new_val logic
        if n > 0:
            self.root = Node((0, n-1))
            self.helper(self.root, arr, 0, n-1)
        # self.init_helper(self.root, arr, 0, n-1)
        # self.init_sums(self.root, arr)
        
    def helper(self, node, arr, left, right):  # No need to do None check, since Node is created
        if left == right:
            node.val = arr[left]
        else:
            mid = (left + right) / 2
            node.left = Node((left, mid))
            node.right = Node((mid+1, right))
            node.val = self.helper(node.left, arr, left, mid) + self.helper(node.right, arr, mid+1, right)
        return node.val

    # def init_helper(self, node, arr, left, right):  # doesn't initialize anything
    #     node = Node((left, right))
    #     if right - left <= 1:
    #         return
    #     mid = (right - left)/2
    #     self.init_helper(node.left, arr, left, mid)  # basically just passing in None
    #     self.init_helper(node.right, arr, mid+1, right)
           
    def init_helper(self, node, arr, left, right):
        # if right - left <= 1:
        if left == right:
            return 
        else:
            mid = (right + left)/2  # if [0, 1], mid = 0 --> [0, 0], [1, 1] --> terminates  
            node.left = Node((left, mid))
            node.right = Node((mid+1, right))
            self.init_helper(node.left, arr, left, mid)
            self.init_helper(node.right, arr, mid+1, right)
      
    def init_sums(self, node, arr):
        if node is None:
            return 0
        left, right = node.span
        if left == right:
            node.val = arr[left]
        # elif right - left == 1:
        #     node.val = arr[left] + arr[right]
        else:
            node.val = self.init_sums(node.left, arr) + self.init_sums(node.right, arr)
        return node.val
        
    def update(self, idx, new_val):   
        if 0 <= idx < len(self.arr):   # handles when arr is length 0
            diff = new_val - self.arr[idx]   # update self.arr
            self.arr[idx] = new_val
            self.update_helper(self.root, idx, diff)

    def update_helper(self, node, idx, diff):
        left, right = node.span  # node should never be None
        # if right - left > 1:
        if right > left:
            mid = (left + right) / 2
            if idx <= mid:
                self.update_helper(node.left, idx, diff)
            else:
                self.update_helper(node.right, idx, diff)
        node.val += diff

    # def update_helper(self, node, idx, new_val):  # uses new_val instead of diff
        # left, right = node.span
        # if left == right:
        #   node.val = new_val
        # # elif right - left == 1:
        # #   node.val = new_val + (arr[right] if left == idx else arr[left])
        # else:
        #   mid = (left + right)/2
        #   if idx <= mid:
        #       node.val = self.update(node.left, idx, new_val)
        #   else:
        #       node.val = self.update(node.right, idx, new_val)
        # return node.val

    def get_sum(self, i, j): 
      if 0 <= i <= j < len(self.arr):   # handles when arr is length 0
          return self.get_sum_helper(self.root, i, j)
      else:
          return None

    def get_sum_helper(self, node, qi, qj):  # Doesn't work, e.g. [1, 2] where search is [1, 3]
        if node is None:
            return 0
        left, right = node.span
        if left >= qi and right <= qj:   # [left, right] is subset of [qi, qj]; only a partial sum
            # print 'Match', qi, qj
            return node.val  
        elif qj < left or qi > right:   # [qi, qj] has no overlap with [left, right]
            return 0
        else:
            mid = (left + right)/2   # node.left has [left, mid]; node.right has [mid+1, right]
            return self.get_sum_helper(node.left, qi, qj) + self.get_sum_helper(node.right, qi, qj)
            """Incorrect"""
            # return self.get_sum_helper(node.left, qi, mid) + self.get_sum_helper(node.right, mid+1, qj)  
            """Saves a few calls, but not much"""
            # if qi > mid:   
            #     return self.get_sum_helper(node.right, qi, qj)
            # elif qj <= mid+1:
            #     return self.get_sum_helper(node.left, qi, qj)

"""New technique - Square Root compression"""
# https://leetcode.com/problems/range-sum-query-mutable/description/  
class Solution2(object):   # "Square Root Decomposition", fastest solution
    
    def __init__(self, nums):  # O(n) preprocessing; O(1) update, O(sqrt(n)) query
        N = len(nums)
        if N > 0:
            x, y = divmod(N, N**0.5)
            self.B_L = int(x) + int(y > 0)
            self.B = [0] * self.B_L
            for i in xrange(N):
                self.B[i / self.B_L] += nums[i]
            self.nums = nums

    def update(self, i, val):
        idx = i / self.B_L
        self.B[idx] += val - self.nums[i]
        self.nums[i] = val

    def sumRange(self, i, j):  # could technically reduce to sqrt(n)/2 by starting from shorter end, but still same big-O
        idx0, idx1 = i / self.B_L, j / self.B_L
        if idx0 == idx1:
            return sum(self.nums[i : j + 1])
        else:
            return sum(self.nums[i: (idx0 + 1) * self.B_L]) + sum(self.B[idx0 + 1 : idx1]) \
                + sum(self.nums[idx1 * self.B_L : j + 1])

arr = [1, 2, 3, 4, 5]
t = SegmentTree(arr)
r = t.root


# class TestSegmentTree(unittest.TestCase):

#     def setUp(self):  # prepares test fixture, always called before each test method
#         arr = [1, 2, 3, 4, 5]
#         self.t = SegmentTree(arr)

#     def tearDown(self): # 
#         pass   # does nothing by default


#     def test_method():  # (all methods must start with 'test')
#         pass

