# https://leetcode.com/problems/all-oone-data-structure/description/

"""
["AllOne", "inc", "dec", "inc", "inc", "getMaxKey", "getMinKey"]
[[], [1], [2], [2], [2], [], []]
["AllOne","inc","inc","inc","inc","inc","inc","dec", "dec","getMinKey","dec","getMaxKey","getMinKey"]
[[],["a"],["b"],["b"],["c"],["c"],["c"],["b"],["b"],[],["a"],[],[]]
"""
from collections import defaultdict
class Solution3(object):   # From fastest solution

    def __init__(self):
        self.dd = collections.defaultdict(int)

    def inc(self, key):
        self.dd[key] += 1

    def dec(self, key):
        if self.dd[key] > 1:
            self.dd[key] -= 1
        else:
            self.dd.pop(key)

    def getMaxKey(self):
        try:
            maxval = max(self.dd.itervalues())
            for i in self.dd:
                if self.dd[i] == maxval:
                    return i
        except:
            return ""

    def getMinKey(self):
        try:
            minval = min(self.dd.itervalues())
            for i in self.dd:
                if self.dd[i] == minval:
                    return i
        except:
            return ""

# import heapq
class Solution2(object):   # Uses regular dicts and deletes empty lists; saves space, but slower than Solution 2

    def __init__(self):
        """The hardest part: updating max if the current max gets decremented."""
        self.keys = {}  # key: current value
        self.values = {}  # values: keys that have that value
        self.max_heap = []  
        self.min_heap = []
        
    def inc(self, key):
        if key not in self.keys:
            new_val = 1
        else:
            old_val = self.keys[key]
            self.values[old_val].remove(key)
            if not self.values[old_val]:  # empty list now
                del self.values[old_val]
                if old_val == self.min_heap[0]:  # originally removed for lazy elimination, but substantially slower if done so
                    heapq.heappop(self.min_heap)
                if old_val == self.max_heap[0]:
                    heapq.heappop(self.max_heap)
            new_val = old_val + 1
        self.keys[key] = new_val
        if new_val in self.values:
            self.values[new_val].append(key)
        else:
            self.values[new_val] = [key]
            heapq.heappush(self.min_heap, new_val)
            heapq.heappush(self.max_heap, -new_val)    
            
    def dec(self, key):
        if key in self.keys:
            old_val = self.keys[key]
            self.values[old_val].remove(key)
            if not self.values[old_val]:
                del self.values[old_val]
                if old_val == self.max_heap[0]:    
                    heapq.heappop(self.max_heap)  
                if old_val == self.min_heap[0]:  
                    heapq.heappop(self.min_heap)
            if old_val == 1:  # Delete from keys and values
                del self.keys[key]
            else:             # Update keys, values, and heaps with new_value
                new_val = old_val - 1
                self.keys[key] = new_val
                if new_val in self.values:
                    self.values[new_val].append(key)    
                else:
                    self.values[new_val] = [key]
                    heapq.heappush(self.min_heap, new_val)
                    heapq.heappush(self.max_heap, -new_val)                             

    def getMaxKey(self):  # arbitrarily return the first element to have reached the max  
        while self.max_heap:
            max_ = -self.max_heap[0]
            if max_ in self.values:
                return self.values[max_][0]  
            else:
                heapq.heappop(self.max_heap)  # dec() handles max elem but not other values
        return ""

    def getMinKey(self):
        while self.min_heap:
            min_ = self.min_heap[0]
            if min_ in self.values:
                return self.values[min_][0]
            else:
                heapq.heappop(self.min_heap)
        return ""

# from collections import defaultdict
# import heapq
class Solution1(object): 

    def __init__(self):
        """The hardest part: updating max if the current max gets decremented."""
        self.keys = defaultdict(int)  # key: current value
        self.values = defaultdict(list)  # values: keys that have that value
        self.max_heap = []  
        self.min_heap = []
        
    def inc(self, key):
        if not self.keys[key]: # changed from "if key not in self.keys" -> now we don't have to delete if a bucket becomes empty
            new_val = 1
        else:   # changed order to be slightly more readable
            old_val = self.keys[key]
            self.values[old_val].remove(key)  # O(k); could use set() for O(1) removal but would then get O(k) add
            if old_val == self.min_heap[0] and not self.values[old_val]:  # Commenting this out -> much slower code
                heapq.heappop(self.min_heap)  # Remove invalid min; will not cover values that aren't min, will be processed lazily
            if old_val == self.max_heap[0] and not self.values[old_val]: 
                heapq.heappop(self.max_heap)
            # if not self.values[old_val]:
            #     del self.values[old_val]
            new_val = old_val + 1
        self.keys[key] = new_val
        if self.values[new_val]:
            self.values[new_val].append(key)    
        else:
            self.values[new_val] = [key]
            heapq.heappush(self.min_heap, new_val)
            heapq.heappush(self.max_heap, -new_val)

    def dec(self, key):
        if self.keys[key]:  # Covers (1) key doesn't exist, (2) value is 0
            old_val = self.keys[key]
            self.values[old_val].remove(key)
            if old_val == self.max_heap[0] and not self.values[old_val]: 
                heapq.heappop(self.max_heap)
            if old_val == self.min_heap[0] and not self.values[old_val]:  # Commenting this out -> much slower code
                heapq.heappop(self.min_heap)  # Remove invalid min; will not cover values that aren't min, will be processed lazily
            # if old_val == 1:  
            #     del self.keys[key]  
            # if not self.values[old_val]:
            #     del self.values[old_val]
            new_val = old_val - 1
            self.keys[key] = new_val
            if new_val > 0:
                if self.values[new_val]:
                    self.values[new_val].append(key)    
                else:
                    self.values[new_val] = [key]
                    heapq.heappush(self.min_heap, new_val)
                    heapq.heappush(self.max_heap, -new_val)

    def getMaxKey(self):  # arbitrarily return the first element to have reached the max  
        while self.max_heap:
            max_ = -self.max_heap[0]
            if self.values[max_]:
                return self.values[max_][0]  
            else:
                heapq.heappop(self.max_heap)  # dec() handles max elem but not other values
        return ""

    def getMinKey(self):
        while self.min_heap:
            min_ = self.min_heap[0]
            if self.values[min_]:
                return self.values[min_][0]
            else:
                heapq.heappop(self.min_heap)
        return ""

"""For Solution1/2, substantial improvement by checking min_heap and max_heap partially instead of complete lazy removal of removed keys"""
# AllOne = Solution1  # 139 ms -> 31.41%  
# AllOne = Solution2  # 155 ms -> 22.31%
AllOne = Solution3  # 72 ms -> 100%

# Your AllOne object will be instantiated and called as such:
# obj = AllOne()
# obj.inc(key)
# obj.dec(key)
# param_3 = obj.getMaxKey()
# param_4 = obj.getMinKey()