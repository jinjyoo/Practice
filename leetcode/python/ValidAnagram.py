# https://leetcode.com/problems/valid-anagram/description/

from collections import Counter

class Solution(object):
    def isAnagram(self, s, t):
        """
        :type s: str
        :type t: str
        :rtype: bool
        """
        # return self.solution1(s, t)  # 95 ms, 38.19%
        # return self.solution2(s, t)  # 59 ms, 90.85%
        return self.solution3(s, t)
    
    def solution1(self, s, t):
        # x = [ord(c)-97 for c in s]  # 48 = ord('a')
        if len(s) != len(t):  # saves time, and takes care of cases where t is subset of s, so doesn't trigger 0 check
            return False
        x = [0]*26
        for c in s:
            x[ord(c) - 97] += 1  
        for c in t:
            idx = ord(c) - 97
            if x[idx] != 0:
                x[idx] -= 1
            else:
                return False
        return True
    
    import string
    def solution2(self, s, t):  # Fastest solution available, somehow...
        if len(s) != len(t):
            return False
        for char in string.ascii_lowercase:
            if s.count(char) != t.count(char):
                return False
        return True

    def solution3(self, s, t):  # Not assuming all lowercase
        if len(s) != len(t):
            return False
        """Method 1"""   # 146 ms, 2.89%; concise but slow
        # would return True if s is strict subset of t, but we know len(s) == len(t)
        # return len(Counter(s) - Counter(t)) == 0       # will always check all of t, then have to subtract again
        """Method 2"""  # 132 ms, 4.55%
        # count = Counter(s)                             
        # for c in t:
        #     if c not in count or count[c] == 0:         # Counter is wrapper for DefaultDict, so same pitfalls
        #         return False
        #     count[c] -= 1
        # return True
        """Method 3"""  # 82 ms, 64.11%
        count = {}
        for c in s:
            try:
                count[c] += 1
            except KeyError:
                count[c] = 1
        for c in t:
            try:
                if count[c] == 0:
                    return False
                count[c] -= 1
            except KeyError:
                return False
        return True
        
    # solution4 - sorting, but that's O(n log n); however, O(1) space if using in-place 
    # ^Some languages will use O(n) space, but can change parameters to pass in list, see Solution explanation  
            
        