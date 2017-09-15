# https://leetcode.com/problems/majority-element/description/

from collections import Counter

class Solution(object):
    def majorityElement(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        # return self.solution1(nums)  #42 ms, 98.61%
        return self.solution2(nums)  # 85 ms, 18.47%  
    
    def solution1(self, nums):  # O(n log n) time, O(1) space
        nums.sort()
        return nums[len(nums)/2]  
    
    def solution2(self, nums):
        return Counter(nums).most_common(1)[0][0]