# https://leetcode.com/problems/sliding-window-median/description/

"""
[1,3,-1,-3,5,3,6,7]
3
[1,1,1,1]
2
[1,2,3,4,2,3,1,4,2]
3
[9,7,0,3,9,8,6,5,7,6]
2
"""
import heapq  # Attempt1
from collections import defaultdict

import bisect  # Solution1
import itertools as it   

from heapq import heappush, heappop  # Solution 2

class Solution(object):  
    
    def medianSlidingWindow(self, nums, k):
        return self.attempt1(nums, k)  # Getting too unwieldy, keep for reference but don't use
        # return self.solution1(nums, k)  # 149 ms -> 94.49%  (used binary search instead of remove())
        # return self.solution2(nums, k)  # 286 ms -> 79.53%
    
    def attempt1(self, nums, k):
        """
        Correctly implemented by Solutions 2/3. Improvements compared to mine:
        (1) no self.window; just keep track of the new number and the number that'll be deleted.
        (2) don't need to keep track of min_size and max_size (which always sum to k), just the overall "balance" 
        (3) handle invalid tops (nums[i-k]) immediately, so you don't have to check before balancing (have to check subsequent top)
            ^ This is probably the error in my code
        """
        res = []  
        self.hmin = []  # bigger half of window
        self.hmax = []  # smaller half of window
        self.window = defaultdict(int)  # do not need {i: num}, since we can tell where a number is on the heap
        self.need_to_delete = defaultdict(int)   
        self.min_size = self.max_size = 0  # stores true size of heap
        for i in xrange(k):
            self.add_num(nums[i])
        res.append(self.get_median())
        for i in xrange(k, len(nums)): 
            if nums[i] not in self.window:
                self.delete_num(nums[i-k])  # nums[i-k] just went out of the window            
                self.add_num(nums[i]) 
            res.append(self.get_median())
        return res
    
    def delete_num(self, num):
        """Problem: What if num is in both hmin and hmax?  Then it must be on top of both, and we arbitrarily invalidate one for hmin."""
        self.window[num] -= 1
        self.need_to_delete[num] += 1
        if self.hmin and num >= self.hmin[0]:  # the num is on the min_heap
            self.min_size -= 1
        else:
            self.max_size -= 1
        # Used to do top validation in get_median, but need to make sure everything is balanced afterward, which relies on add_num
        top1 = self.hmin[0] if self.hmin else None  
        while self.need_to_delete[top1]:
            heapq.heappop(self.hmin)
            self.need_to_delete[top1] -= 1
            top1 = self.hmin[0] if self.hmin else None 
        top2 = -self.hmax[0] if self.hmax else None
        while self.need_to_delete[top2]:
            heapq.heappop(self.hmax)
            self.need_to_delete[top2] -= 1
            top2 = -self.hmax[0] if self.hmax else None
    
    def add_num(self, num):  
        """Since there's one delete for every add, abs(max_size - min_size) <= 2
        Issue: e.g. one 3 is in window, but multiple 3's stored in heap, then only 1 should be valid."""
        self.window[num] += 1         
        if not self.hmin or num > self.hmin[0]:  # no need for hmax clause, will be balanced later
            heapq.heappush(self.hmin, num)
            self.min_size += 1
        else: 
            heapq.heappush(self.hmax, -num)
            self.max_size += 1
        while self.min_size - self.max_size > 1:
            temp = heapq.heappop(self.hmin)
            if self.need_to_delete[temp]:  # temp could also be in self.window, technically (see issue above)
                self.need_to_delete[temp] -= 1
            elif self.window[temp]: 
                heapq.heappush(self.hmax, -temp)
                self.max_size += 1
                self.min_size -= 1              
        while self.max_size - self.min_size > 1:
            temp = -heapq.heappop(self.hmax)
            if self.need_to_delete[temp]:
                self.need_to_delete[temp] -= 1
            elif self.window[temp]:
                heapq.heappush(self.hmin, temp)
                self.min_size += 1
                self.max_size -= 1       
            
    def get_median(self):   # We can assume that k <= len(arr); delete_num -> valid tops, add_num -> balanced heaps
        # print [-i for i in reversed(self.hmax)], self.hmin
        # print self.max_size, self.min_size
        if self.min_size == self.max_size:
            return (self.hmin[0] - self.hmax[0]) / 2.0
        elif self.min_size > self.max_size:
            return self.hmin[0]
        else:
            return -self.hmax[0]
        
    # Similar to: https://discuss.leetcode.com/topic/74634/easy-python-o-nk
    # C++: https://discuss.leetcode.com/topic/74963/o-n-log-k-c-using-multiset-and-updating-middle-iterator
    def solution1(self, nums, k):  # maintain sorted sliding window
        window = sorted(nums[:k])
        is_odd = k&1
        mid = k/2
        medians = []
        medians.append(float(window[mid]) if is_odd else (window[mid-1] + window[mid])/2.0)
        for i in xrange(k, len(nums)):
            del window[bisect.bisect_left(window, nums[i-k])]  # Used to be 428 ms -> 59.06% w/ remove()
            bisect.insort(window, nums[i])
            medians.append(float(window[mid]) if is_odd else (window[mid-1] + window[mid])/2.0)
        return medians     
    
    def solution2(self, nums, k): # Based off: https://discuss.leetcode.com/topic/74634/easy-python-o-nk/9
        medians = []
        hashes = defaultdict(int)
        bheap, theap = [], []
        for i in xrange(k):
            heappush(bheap, nums[i])
        for _ in xrange(k/2, 0, -1):
            heappush(theap, -heappop(bheap))
        medians.append(float(bheap[0]) if k&1 else (bheap[0] - theap[0]) / 2.0)        
        for i in xrange(k, len(nums)):        
            m, n, balance = nums[i-k], nums[i], 0           
            if m >= bheap[0]:  # handle deleting
                balance -= 1
                if m == bheap[0]:  # handle tops now; else we'd have to check top before balancing, then check tops again
                    heappop(bheap)
                else:
                    hashes[m] += 1
            else: 
                balance += 1
                if m == -theap[0]:  
                    heappop(theap)
                else:
                    hashes[m]+=1
            if bheap and n >= bheap[0]:   # handle adding
                balance += 1
                heappush(bheap, n)
            else:
                balance -= 1
                heappush(theap, -n)           
            if balance < 0:  # len(bheap) < len(theap)
                heappush(bheap, -heappop(theap))  # the top of theap/bheap is always valid at this point
            elif balance > 0:
                heappush(theap, -heappop(bheap))              
            while bheap and hashes[bheap[0]]:  # the removed-from heap might have an invalid top, so fix (doesn't change balance)
                hashes[heappop(bheap)] -= 1
            while theap and hashes[-theap[0]]:
                hashes[-heappop(theap)] -= 1 
            medians.append(float(bheap[0]) if k&1 else (bheap[0] - theap[0]) / 2.0)      
        return medians
    
    # Based off: https://discuss.leetcode.com/topic/74679/o-n-log-n-time-c-solution-using-two-heaps-and-a-hash-table/4
    def solution3(self, nums, k):  
        """After changes, basically the same as Solution2, but with more explicit variable names and slightly diff initialization"""
        to_be_deleted, res = defaultdict(int), []
        top_half, bottom_half = nums[:k], []
        heapq.heapify(top_half)
        while len(top_half) - len(bottom_half) > 1:
            heappush(bottom_half, -heappop(top_half))
        res.append(float(top_half[0]) if k&1 else (top_half[0] - bottom_half[0])/2.0)
        for i in xrange(k, len(nums)):
            num, num_to_be_deleted = nums[i], nums[i-k]
            top_bottom_balance = 0
            if num_to_be_deleted >= top_half[0]:
                top_bottom_balance -= 1
                if num_to_be_deleted == top_half[0]:
                    heappop(top_half)
                else:
                    to_be_deleted[num_to_be_deleted] += 1
            else:
                top_bottom_balance += 1
                if num_to_be_deleted == -bottom_half[0]:
                    heappop(bottom_half)
                else:
                    to_be_deleted[num_to_be_deleted] += 1
            if top_half and num >= top_half[0]:
                top_bottom_balance+=1
                heappush(top_half, num)
            else:
                top_bottom_balance-=1
                heappush(bottom_half, -num)
            if top_bottom_balance > 0:
                heappush(bottom_half, -heappop(top_half))
            elif top_bottom_balance < 0:
                heappush(top_half, -heappop(bottom_half))
            while top_half and to_be_deleted[top_half[0]]:
                to_be_deleted[heappop(top_half)] -= 1
            while bottom_half and to_be_deleted[-bottom_half[0]]:
                to_be_deleted[-heappop(bottom_half)] -= 1
                
            res.append(float(top_half[0]) if k&1 else (top_half[0]-bottom_half[0])/2.0)
        return res
            