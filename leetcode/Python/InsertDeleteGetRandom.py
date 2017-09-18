# https://leetcode.com/problems/insert-delete-getrandom-o1/description/

"""
["RandomizedSet","insert","remove","insert","getRandom","remove","insert","getRandom"]
[[],[1],[2],[2],[],[1],[2],[]]
["RandomizedSet","insert","remove","remove","insert","getRandom","remove"]
[[],[3],[3],[0],[3],[],[0]]
"""

import random as rand

class Solution2(object):
    # Java: https://discuss.leetcode.com/topic/53216/java-solution-using-a-hashmap-and-an-arraylist-along-with-a-follow-up-131-ms 
    # C++: https://discuss.leetcode.com/topic/53286/ac-c-solution-unordered_map-vector
    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.vals = []
        self.indexes = {}

    def insert(self, val):
        """
        Inserts a value to the set. Returns true if the set did not already contain the specified element.
        :type val: int
        :rtype: bool
        """
        if val not in self.indexes:
            self.indexes[val] = len(self.vals)
            self.vals.append(val)
            return True
        return False

    def remove(self, val):
        """
        Removes a value from the set. Returns true if the set contained the specified element.
        :type val: int
        :rtype: bool
        """
        if val not in self.indexes:
            return False
        last_val = self.vals[-1]  # could technically check that last_val != len(self.vals)-1
        val_idx = self.indexes[val]  # val_idx is open now, so move last_val there and pop where last_val used to be
        self.vals[val_idx] = last_val     # used to be val
        self.indexes[last_val] = val_idx  # used to be len(self.vals)-1
        self.vals.pop()
        del self.indexes[val]
        return True

    def getRandom(self):
        """
        Get a random element from the set.
        :rtype: int
        """
        return rand.choice(self.vals)

class Solution1(object):

    def __init__(self):
        """
        Add/Delete in O(1) time is easy with sets/dicts.  But sets/dicts, while iterables, are not sequences (no random access)
        
        Other ideas: use heap to extrat earliest index?
        """
        self.members = {}  # record item and the index it maps to in data
        self.data = []
        self.deleted = []   

    def insert(self, val):
        if val not in self.members:
            if self.deleted:
                idx = self.deleted.pop()
                self.members[val] = idx
                self.data[idx] = val
            else:
                self.members[val] = len(self.data)  
                self.data.append(val)
            return True
        return False

    def remove(self, val):
        if val in self.members:
            self.data[self.members[val]] = None
            if len(self.deleted) > 0.7 * len(self.data):  # if self.data is 7/10 None's, then ~3 ops to get valid number, acceptable
                self.data = [elem for elem in self.data if elem is not None]  # O(n) time.  Since members is < 30% of n, relatively small
                for idx, elem in enumerate(self.data):
                    self.members[elem] = idx 
                self.deleted = []
            else:
                self.deleted.append(self.members[val])
                del self.members[val]
            return True
        return False
        
    def getRandom(self):
        n = len(self.data)  # includes deleted elements
        while 1:
            # item = self.data[rand.randint(0, n-1)]  # cannot do something like linear probing, would skew probs towards post-deleted elems
            item = rand.choice(self.data)
            if item is not None:
                return item
        
# RandomizedSet = Solution1  # 152 ms, 70.43%
RandomizedSet = Solution2  # 138 ms, 96.28%  # Fastest solution

# Your RandomizedSet object will be instantiated and called as such:
# obj = RandomizedSet()
# param_1 = obj.insert(val)
# param_2 = obj.remove(val)
# param_3 = obj.getRandom()