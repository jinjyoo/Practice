# https://leetcode.com/problems/longest-substring-without-repeating-characters/description/

'''
"abcabcbb"
"bbbbb"
"pwwkew"
""
"wwppkk"
"c"
"ab"
"aa"
"cdd"
"abba"
'''

class Solution(object):
    def lengthOfLongestSubstring(self, s):  # No assumptions of charset, otherwise could improve with an array (e.g. 128 for ASCII)
        """
        :type s: str
        :rtype: int
        """
        # return self.solution1(s)  # 445 ms, 7.60%
        # return self.solution2(s)  # 115 ms, 39.79%
        return self.solution3(s)  # 82 ms, 88.14%
    
    def solution1(self, s):  # Average case O(n), but worst case O(n^2); could improve by using OrderedDict to avoid rebuilding from scratch
        start = offset = 0  
        curr = start + offset
        res = 0
        seen = {}  # stores the first instance of char in current substring
        while curr < len(s):
            c = s[curr]
            if c in seen:
                res = max(res, offset)  # changed from offset-1; can't use curr char, but e.g. if offset = 1, then 0th char was acceptable
                new_start = seen[c] + 1
                offset -= new_start - start
                start = new_start
                seen = {char : idx for char, idx in seen.iteritems() if idx >= new_start}
                # print start, offset, res, seen
            seen[c] = curr
            offset += 1
            curr += 1
        return max(res, offset)  # in case all unique chars
    
    def solution2(self, s):  # O(n) time, O(n) space
        if not s: return 0
        dp = [0]*len(s)  #dp[i] is length of longest starting at i
        dp[-1] = 1  
        tails = {s[-1]: len(s)-1}  # index of earliest seen instance of c in s, calculated from the back
        res = 1  # technically don't need res, but faster than max(dp)
        for i in reversed(xrange(len(s)-1)):
            c = s[i]
            if c in tails:
                dp[i] = min(dp[i+1] + 1, tails[c] - i) # [i, tails[c])  # added min check for cases like "abba"
            else:
                dp[i] = dp[i+1] + 1   
            # dp[i] = tails.get(c, len(s)) - i  # can't do this because we lose the check for repeats from back in the string
            tails[c] = i
            res = max(res, dp[i])
        return res  

    def solution3(self, s):  # From: https://discuss.leetcode.com/topic/11632/a-python-solution-85ms-o-n  (similar to shortest)
        start = res = 0
        seen = {}
        for idx, c in enumerate(s):
            if c in seen and start <= seen[c]:  # need the second condition for cases like "abba"
                start = seen[c] + 1
            else:  # else optimization not in shortest
                res = max(res, idx - start + 1)  # [left, i]  
            seen[c] = idx  # t stores most recent instance of t
        return res
            
        