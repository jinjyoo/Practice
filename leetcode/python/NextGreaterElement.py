# https://leetcode.com/problems/next-greater-element-i/description/

"""
[4,1,2]
[1,3,4,2]
"""

from collections import defaultdict

class Solution(object):
    def nextGreaterElement(self, findNums, nums):
        """
        :type findNums: List[int]
        :type nums: List[int]
        :rtype: List[int]
        
        Naive way: hashtable for nums, then starting from each idx, search for next biggest; O(n) + O(mn/2) = O(mn)
        """
        # return self.solution1(findNums, nums)   # 112 ms -> 33.83%    
        # return self.solution2(findNums, nums)  # 65 ms -> 61.58%
        # return self.attempt(findNums, nums)
        # return self.solution3(findNums, nums)  # 52 ms -> 76.00%
        return self.solution4(findNums, nums)  # 69 ms -> 65.75%  
    
    def solution4(self, findNums, nums):  #O(len(nums)) time, but O(len(findNums)) space
        check, stack = {fnum:-1 for fnum in findNums}, []  # initialization takes more time
        for num in nums:     
            while stack and num > stack[-1]:
                check[stack.pop()] = num
            if num in check:  
                stack.append(num)
        ret = []
        return [check[fnum] for fnum in findNums]
    
    # Modified from: https://discuss.leetcode.com/topic/77916/java-10-lines-linear-time-complexity-o-n-with-explanation
    # Cannot do solution4's space optimization since we don't know what's in findNums (w/o initialization -> no need for defaultdict)
    def solution3(self, findNums, nums):  # O(len(nums)) time, O(len(nums)) space
    	"""
    	Stack will keep a *decreasing* subsequence.
		[9, 8, 2, 1] and then we see 6 which is greater than 1 so pop 1, 2 whose next greater element should be 6
    	"""
        check, stack = defaultdict(lambda: -1), []
        for num in nums:     
            while stack and num > stack[-1]:  # keep popping off smaller elements so we can insert num, for decreasing seq
                check[stack.pop()] = num
            stack.append(num)  # at end of loop, everything in stack never found something bigger -> set to -1
        return [check[fnum] for fnum in findNums]
    
    
    def solution2(self, findNums, nums):  # Naive solution with optimization
        if not findNums: return []
        idxs = {}
        for i, num in enumerate(nums, 0):
            idxs[num] = i
        res = []
        for fnum in findNums:
            for i in xrange(idxs[fnum]+1, len(nums)):
                if nums[i] > fnum:
                    res.append(nums[i])
                    break
            else:
                res.append(-1)
        return res
                    
    def solution1(self, findNums, nums):  # O(n^2) time, O(n) space   # Super naive solution
        if not findNums or not nums: return [] 
        ret = []
        for num in findNums:
            ind = nums.index(num)  # do not need to check for value errors
            for i in xrange(ind+1, len(nums)):
                if nums[i] > num:
                    ret.append(nums[i])
                    break
            else:  # loop-else construction
                ret.append(-1)
        return ret       
            
         
    def attempt(self, findNums, nums):
        """Fails because e.g. nums = [1, 3, 4, 2], for 1 it should be 3, not 4"""
#         if not findNums:
#             return []
#         curr_max = nums[-1]
#         maxes = {curr_max : -1}
#         for i in xrange(len(nums)-2, -1, -1):
#             if nums[i] > curr_max:   
#                 maxes[nums[i]] = -1  # nums[i] didn't have anything bigger than it
#                 curr_max = nums[i]
#             else: # nums[i] < curr_max; no == since no duplicates
#                 maxes[nums[i]] = curr_max
#         print maxes
#         return [maxes[fnum] for fnum in findNums]
    
        """Fails because e.g. nums = [4, 1, 2, 3], for 1 it should be 2"""
        if not findNums:
            return []
        maxes = defaultdict(lambda: -1)  # store maximum for nums (NOT findNums)
        curr_max = nums[0]
        for i in xrange(1, len(nums)):  
            if nums[i] > curr_max:
                maxes[curr_max] = nums[i]  # nums[i] is the first number found bigger than curr_max
                curr_max = nums[i]
            # else: if this number is smaller, then it wouldn't have provided a solution for any numbers before curr_max
        return [maxes[fnum] for fnum in findNums]       
            
    
    
    
    
    
    
