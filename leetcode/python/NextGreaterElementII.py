# https://leetcode.com/problems/next-greater-element-ii/description/

from collections import defaultdict
# from collections import deque   
import itertools as it
# import bisect

class Solution(object):
    def nextGreaterElements(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        
        Naive: rotate, then use super-naive solution from problem 1, since that didn't rely on duplciates (no hash tables) -> O(n^2)
        """
        # return self.solution1(nums)  # 289 ms -> 71.03%  
        # return self.solution2(nums)   # 259 ms -> 96.10%
        # return self.solution3(nums)  # 262 ms -> 94.71%  
        return self.solution4(nums)  # 299 ms -> 61.28%  
    
    def solution4(self, nums):  # Not sure why this is slower than even the O(n log n), one extra indexing shouldn't be that extreme
        """Using the stack trick in solution3 + solution2's logic; one extra __getitem__ but less space complexity"""
        if not nums: return []
        res = [-1]*len(nums)
        queue = [nums[0]]
        stack = [0]
        for i, num in enumerate(it.islice(nums, 1, None), 1):
            if queue[-1] < num:
                queue.append(num)
            while stack and nums[stack[-1]] < num:
                res[stack.pop()] = num
            stack.append(i)
        q_ptr = 0
        while q_ptr < len(queue):  # stack is decreasing and queue is increasing
            while stack and nums[stack[-1]] < queue[q_ptr]:
                res[stack.pop()] = queue[q_ptr]
            q_ptr += 1
        for i in stack:
            res[i] = -1
        return res
    
    def solution3(self, nums):  # From: https://discuss.leetcode.com/topic/81168/python-6-lines-solution-using-stack/7
        """Unlike my solution, stack just stores the indexes; can easily check num[i] from nums itself."""
        stack, res = [], [-1] * len(nums)
        for i in xrange(len(nums)):
            while stack and (nums[stack[-1]] < nums[i]):
                res[stack.pop()] = nums[i]
            stack.append(i)
        for i in xrange(len(nums)):  # repeat again, using the same stack
            while stack and (nums[stack[-1]] < nums[i]):
                res[stack.pop()] = nums[i]
            if stack == []:    
                break
        return res
    
    def solution2(self, nums):
        """Same logic as solution1, but realization that binary search is not needed; queue is increasing, deque is decreasing.
        Slight optimization over just iterating through the whole nums again.
        """
        if not nums: return []
        res = [-1]*len(nums)
        queue = [nums[0]]
        # queue = deque((nums[0],))  # much slower (300+ ms) when using deque and popleft() instead of q_ptr
        stack = [(0, nums[0])]
        for i, num in enumerate(it.islice(nums, 1, None), 1):
            if queue[-1] < num:
                queue.append(num)
            while stack and stack[-1][1] < num:
                res[stack.pop()[0]] = num
            stack.append((i, num))
        q_ptr = 0
        while q_ptr < len(queue):  # stack is decreasing and queue is increasing
            while stack and stack[-1][1] < queue[q_ptr]:
                res[stack.pop()[0]] = queue[q_ptr]
            q_ptr += 1
        for i, num in stack:
            res[i] = -1
        return res
    
    def solution1(self, nums):  # O(n log n)
        """Idea: keep stack like in previous problem, but also keep a queue of strictly increasing subsequence
        queue[-1] (biggest element, might have multiple) has no bigger number; for everything with -1, check just queue with bin. search
        """
        if not nums: return []
        res = [-1]*len(nums)
        stack = [(0, nums[0])]
        # queue = [(0, nums[0])]  # deque(((0, nums[0]))   # we never pop, so technically don't need "queue"
        # queue_idxs.append(i)  # actually, don't need indexes
        queue = [nums[0]]  # store the LIS that starts with nums[0]
        for i, num in enumerate(it.islice(nums, 1, None), 1):  # start from 1 so I can avoid "if queue" checks
            if queue[-1] < num:  
                queue.append(num)  # queue does NOT have duplicates; only stores first occurrence
            # else:  
            while stack and stack[-1][1] < num:
                res[stack.pop()[0]] = num
            stack.append((i, num))  # stack could have duplicates
        # print stack, '\n', queue
        for i, num in stack:  # everything not set; queue should be subset of stack
            try:
                res[i] = queue[bisect.bisect_right(queue, num)]  
            except IndexError:   # bigger_idx = len(queue)+1, so num == max(queue)
                res[i] = -1            
            # next_biggest = queue[Solution.binary_search(queue, num, 0, i)]  # check to left of num, since right didn't have anything
        return res                
    
    # @staticmethod
    # def binary_search(arr, target, low, high):   # assumes arr is tuple, with key = arr[1]
    #     target += 1   # find the next biggest
    #     while low < high:  # [low, high)
    #         mid = (low + high)/2
    #         if arr[mid][1] > target:
    #             low = mid + 1
    #         elif arr[mid][1] < target:
    #             high = mid
    #         else:
    #             return mid  
    #     return mid  # not -1; target+1 might not be in arr, but we want this index   
    
    def idea1(self, nums):  # possibly try later
        """
        Idea: take [10, 1, 3, 11, 5], and have the array in advance (we know the size will be len(nums), and set default to -1)
        10: [10], {10: -1}  *note: stack also stores idx of num, not shown 
        1: [10, 1], {10: -1, 1:0}; if item < stack[-1], then worst case, item's biggest item to right with wrap-around is stack[-1] 
        3: [10, 3], {10: -1, 3:0}; pop everything off stack < 3, since 3 is the answer.  If 3 is the only thing on stack, then 3:-1, but 
            otherwise, in worst-case, 3's left neighbor (10, idx=0) would be answer on wrap-around.  Set nums[idx] = ans, delete from dict
            (alternatively, could just check if -1 in final array at end, signifying it was never set)
        11: [11], {11: -1}; pop off 3 and 10
        5: [11, 5], {11: -1, 5: idx(11) = 3}   
        """
        if not nums:
            return []
        res = [-1]*len(nums)
        stack = []  # store (idx, value); also deals with duplicates
        idxs = {}
        for i, num in enumerate(nums):
            while stack and stack[-1][1] < num:  # will take care of duplicates on stack
                # idx, val = stack.pop()
                # for sub_idx in idxs[val]:
                #     res[idx]
                res[stack.pop[0]] = num
                del idxs[num]
            if stack:  
                if stack[-1][0] > idxs[num]: 
                    idxs[num] = stack[-1][0]  # worst case, id of the biggest number that stopped the popping
                # else:  # ==   
                    # idxs[num] = idxs[num]   # e.g. [11, 10, 1, 10], nothing > 10 in between the two 10's, so left's answer == right's
                    # Note: don't think about as right's answer == left, e.g. # [12, 11, 10, 1, 10]
            stack.append((i, num))
        return res
            
    
    def attempt(self, nums):    # Didn't notice that there are duplicates allowed, unlike in previous problem
        """
        Naive: reorder so that max is at end, then treat like non-circular (previous problem) -> O(n) time
        This should work even if there are multiple max_val items (edit: but not multiple items in general)
        """
        if not nums:
            return []
        max_idx, max_val = 0, nums[0]
        for i in xrange(1, len(nums)):
            if max_val < nums[i]:
                max_idx, max_val = i, nums[i]
        rotated = nums[max_idx+1:] + nums[:max_idx+1]
        check, stack = defaultdict(lambda: -1), []
        for num in rotated:
            while stack and num > stack[-1]:
                check[stack.pop()] = num
            stack.append(num)  # stack is nonincreasing order
        return [check[num] for num in nums]  # need to preserve original nums
    

            