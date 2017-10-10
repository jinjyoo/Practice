# https://leetcode.com/problems/range-sum-query-mutable/description/

"""
["NumArray","sumRange","update","sumRange"]
[[[1,3,5]],[0,2],[1,2],[0,2]]
["NumArray"]
[[[]]]
"""
# https://leetcode.com/articles/range-sum-query-mutable/#approach-2-sqrt-decomposition-accepted
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
            return sum(self.nums[i: (idx0 + 1) * self.B_L]) + sum(self.B[idx0 + 1 : idx1]) + sum(self.nums[idx1 * self.B_L : j + 1])

class Solution1(object):   # O(n) preprocessing; O(log n) update/query

    def __init__(self, nums):
        self.tree = SegmentTree(nums)

    def update(self, i, val):
        self.tree.update(i, val)
        
    def sumRange(self, i, j):
        return self.tree.get_sum(i, j)
        
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
        
    def update(self, idx, new_val):   
        if 0 <= idx < len(self.arr):   # handles when arr is length 0
            diff = new_val - self.arr[idx]   # update self.arr
            self.arr[idx] = new_val
            self.update_helper(self.root, idx, diff)

    def update_helper(self, node, idx, diff):
        left, right = node.span  # node should never be None
        if right > left:
            mid = (left + right) / 2
            if idx <= mid:
                self.update_helper(node.left, idx, diff)
            else:
                self.update_helper(node.right, idx, diff)
        node.val += diff

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
            return node.val  
        elif qj < left or qi > right:   # [qi, qj] has no overlap with [left, right]
            return 0
        else:
            mid = (left + right)/2   # node.left has [left, mid]; node.right has [mid+1, right]
            return self.get_sum_helper(node.left, qi, qj) + self.get_sum_helper(node.right, qi, qj)
        
# NumArray = Solution1   # 335 ms -> 38.71%        
NumArray = Solution2   # 88 ms -> 99.71%
        
        
# Your NumArray object will be instantiated and called as such:
# obj = NumArray(nums)
# obj.update(i,val)
# param_2 = obj.sumRange(i,j)