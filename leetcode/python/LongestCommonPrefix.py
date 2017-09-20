# https://leetcode.com/problems/longest-common-prefix/description/

class Solution(object):
    def longestCommonPrefix(self, strs):
        """
        :type strs: List[str]
        :rtype: str
        """
        # return self.solution1(strs)  # 42 ms -> 54.90%
        return self.solution4(strs)  # 36 ms -> 87.91%  
#         if not strs:
#             return ""
#         i = 0  # rather janky - address [""], since i is never defined if the for-loop never runs; i o/w gets reassigned
#         base = strs[0]
           
        
#         for i, c in enumerate(base, 0):
#             for j in xrange(1, len(strs)):  # for str in strs[1:]  
#                 # trunc = strs[:len(first)]
#                 try:
#                     if base[i] != strs[j][i]:
#                         i -= 1
#                         break
#                 except IndexError as e:
#                     break
                
#         for i, c in enumerate(strs[0], 0):
#             for j in xrange(1, len(strs)):
#                 if i == len(strs[j]) or strs[0][i] != strs[j][i]:
#                     break
#         return strs[0][:i+1]

    # Modified from: https://discuss.leetcode.com/topic/6987/java-code-with-13-lines/12
    def solution1(self, strs):  
        if len(strs) == 0: return ''
        prefix = strs[0]
        for i in xrange(1, len(strs)):
            while not strs[i].startswith(prefix):
                prefix = prefix[:-1]
        return prefix
    
    def solution2(self, strs):  # Modified from: https://discuss.leetcode.com/topic/6308/simple-python-solution/2
        return reduce(self.lcp, strs) if strs else ''
    
    def lcp(self, str1, str2):
        for i in xrange(min(len(str1), len(str2))):
            if str1[i] != str2[i]:
                break
        return str1[:i]        
    
    def solution3(self, strs):  # Modified from my original solution
        if len(strs) == 0:
            return ''
        if len(strs) == 1:
            return strs[0]
        strs.sort()  # lexicographically
        # s, t = (strs[0], strs[-1]) if len(strs[0]) <= len(strs[1]) else (strs[-1], strs[0])
        s, t = strs[0], strs[-1]
        for i in xrange(min(len(s), len(t))):
            if s[i] != t[i]:
                break
        return s[:i]
    
    def solution4(self, strs):  # From fastest solution
        if len(strs) == 0:
            return ''
        elif len(strs) == 1:
            return strs[0]
        mins = min(strs, key=len)  # shortest string
        i = 0
        n = len(mins)
        while i < len(strs):
            if mins[:n] != strs[i][:n]:
                n -= 1
                i = 0
            else:
                i += 1
        return mins[:n]
    
        