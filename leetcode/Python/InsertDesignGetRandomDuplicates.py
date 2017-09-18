# https://leetcode.com/problems/insert-delete-getrandom-o1-duplicates-allowed/description/

import random
# import bisect

class Solution3(object):  # Version of Solution 2 with list instead of set, slightly faster

    def __init__(self):
        self.vals = []
        self.idxs = collections.defaultdict(list)    # Fast append at the cost of slower remove, but net gain
        
    def insert(self, val):
        self.idxs[val].append(len(self.vals))
        self.vals.append(val)
        return len(self.idxs[val]) == 1
        
    def remove(self, val):
        if self.idxs[val]:
            out, ins = self.idxs[val].pop(), self.vals[-1]
            self.vals[out] = ins
            if self.idxs[ins]:
                self.idxs[ins].append(out)  
                self.idxs[ins].remove(len(self.vals)-1)  
            self.vals.pop()
            return True
        return False 

    def getRandom(self):
        return random.choice(self.vals)

class Solution2(object):  # Modified from: https://discuss.leetcode.com/topic/53896/frugal-python-code

    def __init__(self):
        self.vals = []
        self.idxs = collections.defaultdict(set)  # use sets instead of lists
        
    def insert(self, val):
        self.idxs[val].add(len(self.vals))
        self.vals.append(val)
        return len(self.idxs[val]) == 1
        
    def remove(self, val):
        if self.idxs[val]:
            out, ins = self.idxs[val].pop(), self.vals[-1]
            self.vals[out] = ins
            if self.idxs[ins]:
                self.idxs[ins].add(out)  # have to add before remove in case ins == val and out == len(self.vals)-1
                self.idxs[ins].discard(len(self.vals)-1)    # Unlike with lists, this is done in O(1) time
            self.vals.pop()                                 # However, this comes at the cost of slower adds() 
            return True
        return False 

    def getRandom(self):
        return random.choice(self.vals)

class Solution1(object):
    
    def __init__(self):
        self.nums = {}  # map num -> idx in data
        self.data = []  # idx -> num
        
    def insert(self, val):
        self.data.append(val)
        if val in self.nums:  # since we need to check this anyway, didn't use a defaultdict
            self.nums[val].append(len(self.data)-1)
            return False
        else:
            self.nums[val] = [len(self.data)-1]
            return True

    def remove(self, val):
        if val not in self.nums:
            return False
        idx = self.nums[val].pop()   # delete the most recent addition
        if not self.nums[val]: 
            del self.nums[val]
        last_val = self.data[-1]
        if val != last_val:   # if ==, we can just delete the most recent data, no need to do any switch and replace
            self.data[idx] = last_val
            # self.nums[last_val][-1] = idx   ### Problem: idx might not be most recently added instance of last_val
            lst = self.nums[last_val]  # e.g. remove(3) (idx=3), last_val 5 (idx=10) is shifted to 3, but most recent 5 had been 4th element
            if lst[-1] > idx:          # since idx isn't in lst, insort left/right doesn't matter
                bisect.insort(lst, idx)    # O(log k), but this is only for this specific case, and k should usually be small                 
            lst.pop() ### Don't forget to pop
        self.data.pop()                 
        return True

        # if len(self.data) == 1:  # Fixes bug where val == last_val and len(data) == 1, since we delete and add it in again
        #     self.data.pop()
        #     del self.nums[val]
        # else:
        #     idx = self.nums[val].pop()   # delete the most recent addition
        #     last_val = self.data[-1]  
        #     self.data[idx] = last_val
        #     try:  # Error if val == last_val and val was the only item in the list
        #         self.nums[last_val][-1] = idx  # last_val's idx should've been most recent one added to nums, so always -1
        #     except IndexError:
        #         self.nums[last_val] = [idx]
        #     self.data.pop()
        #     if not self.nums[val]: 
        #         del self.nums[val]
        
    def getRandom(self):
        return random.choice(self.data)

# RandomizedCollection = Solution1  # 152 ms -> 78.01%
# RandomizedCollection = Solution2  # 145 ms -> 90.38%
RandomizedCollection = Solution3  # 139 ms -> 95.53
    
# Your RandomizedCollection object will be instantiated and called as such:
# obj = RandomizedCollection()
# param_1 = obj.insert(val)
# param_2 = obj.remove(val)
# param_3 = obj.getRandom()