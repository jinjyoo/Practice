# Alias for LRUCache; refine later to be more general.

"""
["LRUCache","put","put","get","put","get","put","get","get","get"]
[[2],[1,1],[2,2],[1],[3,3],[2],[4,4],[1],[3],[4]]
["LRUCache","put","put","get","put","put","get"]
[[2],[2,1],[2,2],[2],[1,1],[4,1],[2]]
"""

from collections import OrderedDict
class Solution3(object):    # Modified from: https://discuss.leetcode.com/topic/3831/very-short-solution-using-python-s-ordereddict
    # Java version: https://discuss.leetcode.com/topic/43961/laziest-implementation-java-s-linkedhashmap-takes-care-of-everything
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = collections.OrderedDict()

    def get(self, key):
        if not key in self.cache:
            return -1
        value = self.cache.pop(key)
        self.cache[key] = value
        return value

    def put(self, key, value):
        if key in self.cache:  # old item -> pop it, we'll add it on again
            self.cache.pop(key)   
            # self.cache.move_to_end(key, last=True)  # only in Python 3.2+; don't need to pop and add
        elif len(self.cache) == self.capacity:  # new item, get rid of something
            self.cache.popitem(last=False)  # pop the first item, the least recently used
        self.cache[key] = value

# from collections import deque  
class Solution2(object):  # Modified from fastest solution  # Uses deque

    def __init__(self, capacity):
        self.cache = {}
        self.dq = deque()
        self.capacity = capacity

    def get(self, key):  
        if key not in self.cache: 
            return -1
        self.dq.append(key)      # another copy of key put on the deque, update
        self.cache[key][1] += 1  # number of "copies" in heap
        return self.cache[key][0]
    
    def put(self, key, value):
        self.dq.append(key)
        if key not in self.cache:
            self.cache[key] = [value, 1]
        else:
            self.cache[key][0] = value  # update value
            self.cache[key][1] += 1
        if len(self.cache) > self.capacity:
            while 1:            
                k = self.dq.popleft()
                self.cache[k][1] -= 1  # we just removed a copy from the heap; but if > 0 still, then it was updated some point later
                if self.cache[k][1] == 0:  # we don't append k back even if it still has a reference
                    del self.cache[k]
                    return
                
# import heapq
# import itertools as it
class Solution1(object):  # Uses Heap

    def __init__(self, capacity):  
        self.heap = []  # push (time, value) 
        self.entries = {}
        self.counter = it.count(0)  # count will go up - the higher, the more recent -> don't pop it
        self.capacity = capacity
        # self.num_zombies = 0   # number of values deleted from entries but still somewhere in heap
    
    def get(self, key):
        if key not in self.entries:
            return -1
        else:
            data = self.entries[key][-1]
            self.put(key, data)  # need to update priority by putting it in cache again
            return data
        
    def put(self, key, value):  
        if key in self.entries:  # On updates, entries will NOT change size, so we won't call pop and accidentally get rid of something
            old_entry = self.entries.pop(key)  
            old_entry[-1] = None   # modify it on the heap, lazily delete 
        entry = [next(self.counter), key, value]
        self.entries[key] = entry 
        heapq.heappush(self.heap, entry)
        if len(self.entries) > self.capacity: 
            self.pop()                               
        
    def pop(self):  # the cache will never just pop, will only pop in response to a push; heap has >= 1 non-None entry
        while self.heap:
            # priority, key, value = heapq.heapreplace(self.heap, entry)  # Error: should only push once; just do pop and push separately
            _, key, value = heapq.heappop(self.heap)
            if value is not None:
                return self.entries.pop(key)
        # raise KeyError('Heap is empty.')

# LRUCache = Solution1  # 275 ms -> 50.65%   
# LRUCache = Solution2  # 202 ms -> 98.33%    
LRUCache = Solution3   # 282 ms -> 46.65%  

"""
Other solutions:  Doubly-linked-list: 
https://discuss.leetcode.com/topic/6613/java-hashtable-double-linked-list-with-a-touch-of-pseudo-nodes/12?page=1
"""

# Your LRUCache object will be instantiated and called as such:
# obj = LRUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)

