# https://leetcode.com/problems/shuffle-an-array/description/

import itertools as it
import random 
 

class Solution3(object):  # From: https://discuss.leetcode.com/topic/54049/python-hack
    def __init__(self, nums):
        self.reset = lambda: nums
        self.shuffle = lambda: random.sample(nums, len(nums))

class Solution2(object):  # Improved to 712 ms -> 88.71% from 805 ms -> 53.88%, by using random() instead of randint()
    def __init__(self, nums):  # Similar to fastest solution
        self.original = nums
        
    def reset(self):
        return self.original
        
    def shuffle(self):  # I don't think it's biased, but definitely slower in logic than Fisher-Yates
        n = len(self.original)
        res = self.original[:]
        for i in xrange(n):
            # j = random.randint(0, n-1)  # much slower with this
            j = int(n * random.random())
            res[i], res[j] = res[j], res[i]
        return res    
        # res = [None]*n
        # indices = {i for i in xrange(n)}
        # https://stackoverflow.com/questions/10432022/in-python-is-set-pop-deterministic -> could be deterministic for Py2
        # for i in xrange(n):
        #     res[indices.pop()] = self.original[i]  # unclear of time complexity of set.pop()
    
    def shuffle(self):    # Fisher-Yates
        res = self.original[:]
        for i in xrange(len(ans)-1, 0, -1):    # start from end
            j = random.randrange(0, i+1)       # Alternatively: random.randomrange(i, n+1), going forward
            ans[i], ans[j] = ans[j], ans[i]    
        return ans

class Solution1(object): # Trivial solution with built-ins; Problem -> not every solution can be generated for long sequences
    # 689 ms -> 95.29%; Boosted from 735 ms -> 80.23% by shuffling previous temp instead of shuffling original
    # Per: https://discuss.leetcode.com/topic/53984/reset-makes-no-sense/2, we should be shuffling original array, not previous shuffled
    def __init__(self, nums):
        """
        :type nums: List[int]  
        """
        self.original = nums
        self.temp = nums[:]
        
    def reset(self):
        """
        Resets the array to its original configuration and return it.
        :rtype: List[int]
        """
        return self.original
        
    def shuffle(self):
        """
        Returns a random shuffling of the array.  
        :rtype: List[int]
        """
        # return next(it.permutations(self.original))  # deterministic; and expensive to calculate the n! possibilities and return one
        random.shuffle(self.temp)  
        return self.temp
     
# Solution = Solution1  # 689 ms -> 95.29%
Solution = Solution2  # 712 ms -> 88.71%
        
# Your Solution object will be instantiated and called as such:
# obj = Solution(nums)
# param_1 = obj.reset()
# param_2 = obj.shuffle()