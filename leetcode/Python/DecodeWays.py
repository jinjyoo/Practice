# https://leetcode.com/problems/decode-ways/description/

# import functools

# def memo(func):
#     cache = {}
#     @functools.wraps(func)
#     def wrapper(self, *args):
#         if args not in cache:
#             cache[args] = func(self, *args)
#         return cache[args]
#     return wrapper
"""
""
"1279243"
"1"
"2222"
"0123"
"1023"
"1000"
"101"
"1001001101001010101010010111010"
"103041020106070101090181010"
"""
class Solution(object): 
    """Similar to Fibonacci/stairs."""
    def numDecodings(self, s):
        """
        :type s: str
        :rtype: int
        """
        # return self.solution1(s)  # 58 ms, 16.45%
        # return self.solution2(s)  # 46 ms, 46.57%
        # return self.solution3(s)  # 42 ms, 62.64%
        return self.solution4(s)  # 32 ms, 99.80%  
    
    def solution1(self, s):  # 58 ms, 16.45%; O(n) time and space, Top-Down Recursion
        if not s or s[0] == '0':
            return 0
        self.cache = {}  # technically could just use an array
        return self.helper(s, 0)  # easier to think about moving right than left, though slightly more verbose
    
    def helper(self, s, n):  
        if n not in self.cache:   
            if n == len(s) or s[n] == '0':
                self.cache[n] = 0
            elif n == len(s)-1:
                self.cache[n] = 1
            elif n == len(s)-2:
                self.cache[n] = int(int(s[n:n+2]) <= 26) + self.helper(s, n+1)
            else:
                self.cache[n] = self.helper(s, n+1) + (self.helper(s, n+2) if int(s[n:n+2]) <= 26 else 0)
        return self.cache[n]
    
    def solution2(self, s):  # Modified from: https://discuss.leetcode.com/topic/7823/accpeted-python-dp-solution
        if not s or s[0] == '0': return 0
        dp = [0]*(len(s)+1)
        dp[0] = dp[1] = 1  # base case for length 1/2 
        for i in xrange(2, len(s)+1):  # for s, starts from 1; already confirmed s[0] is valid
            if s[i-1] != "0":
                dp[i] += dp[i-1]  # else 0
            if '10' <= s[i-2:i] <= '26':
                dp[i] += dp[i-2]
        return dp[-1]
    
    # Modified from: https://discuss.leetcode.com/topic/4727/concise-cpp-solution-with-o-1-space-and-o-n-time/2
    def solution3(self, s):  
        if not s or s[0] == '0': return 0
        pre2, pre1 = 1, 1  # pre<i> means dp[curr-i]
        for i in xrange(1, len(s)):
            x = pre1 if s[i] != '0' else 0
            y = pre2 if int(s[i-1 : i+1]) <= 26 and s[i-1] != '0' else 0
            pre1 = x + y
            pre2 = x
        return pre1
        
    # From the fastest solution (32 ms)
    def solution4(self, s):  # Speed things by avoiding redundant '0' checks 
        if s == "":
            return 0
        pre, cur, pre_num = 1, 1, 0
        for idx in xrange(len(s)):           
            num = ord(s[idx]) - 48  # chr(48) = '0'
            tmp = 0
            if pre_num != 0 and pre_num * 10 + num <= 26:
                tmp += pre
            if num != 0:
                tmp += cur           
            pre, cur, pre_num = cur, tmp, num      
        return cur
        
    # def attempt1(self, s):  # forgot about 0s, sadly
    #     n = len(s)
    #     if n < 2:
    #         return n
    #     res = 1
    #     for i in xrange(n-1):
    #         if int(s[i:i+2]) <= 26:
    #             res += 1
    #     return res

        