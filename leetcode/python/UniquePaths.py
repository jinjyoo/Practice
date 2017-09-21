# https://leetcode.com/problems/unique-paths/description/

from collections import defaultdict
from collections import deque
import math

class Solution(object):
    def uniquePaths(self, m, n):
        """
        :type m: int
        :type n: int
        :rtype: int
        """
        return self.solution0(m, n)  # 29 ms -> 94.93%, 
        # return self.solution1(m, n)  # 65 ms -> 4.41%
        # return self.solution2(m, n)  
        # return self.solution3(m, n)  # 32 ms -> 74.59%
        # return self.solution4(m, n)  # 32 ms -> 74.59%
        
    def solution0(self, m, n):  
        """Just a math problem, find combinations of a string made of m-1 D's and n-1 W's -> (n+m-2 choose m-1)"""
        # if m <= 0 or n <= 0:  # 49 ms -> 13.02%, but improved using built-in factorial function
        #     return 0
        # k = n+m-2   # 
        # prod = 1
        # fact = 1
        # for i in xrange(m-1):
        #     prod *= k-i
        #     fact *= i+1
        # return prod / fact
    
        f = math.factorial
        return f(m+n-2)/f(m-1)/f(n-1)
    
    def solution1(self, m, n):
        self.cache = defaultdict(int)
        return self.dfs(m-1, n-1)  # starting on (1, 1); could change to (0, 0)
        
    def dfs(self, m, n):
        if (m, n) not in self.cache:
            if m == 0 or n == 0:  # OR, since once m reaches 0, can only go right; and vice versa
                self.cache[(m, n)] = 1
            else:
                if m > 0:
                    self.cache[(m, n)] += self.dfs(m-1, n)
                if n > 0:
                    self.cache[(m, n)] += self.dfs(m, n-1)
        return self.cache[(m, n)]
    
    # def solution2(self, m, n):
    #     res = 0
    #     # cache = defaultdict(int)
    #     queue = deque(((m-1, n-1),))
    #     while queue:
    #         i, j = queue.popleft()
    #         # if (i, j) in visited: continue
    #         if (i, j) in cache:
    #             res += cache[(i, j)]
    #         if i == 0 or j == 0:
    #             cache[(i, j)] = 1
    #         else:
    #             if i > 0:
    #                 queue.append((i-1, j))
    #             if j > 0:
    #                 queue.append((i, j-1))
    #     return cache[(m-1, n-1)]
    
    def solution3(self, m, n):
        if m <= 1 or n <= 1:
            return 1
        dp = [[0]*n for _ in xrange(m)]
        dp[-1][:] = [1]*n  
        for i in xrange(m-1):
            dp[i][-1] = 1
        for i in xrange(m-2, -1, -1):
            for j in xrange(n-2, -1, -1):
                dp[i][j] = dp[i+1][j] + dp[i][j+1]
        return dp[0][0]
    
    def solution4(self, m, n):
        if m <=1 or n <= 1:
            return 1
        # if m < n: return self.solution4(n, m)  # could make this O(min(m, n)) space  
        dp = [1]*n  # initialize bottom row of table
        for i in xrange(m-2, -1, -1):
            for j in xrange(n-2, -1, -1):
                # dp[j] = dp[j] + dp[j+1]
                dp[j] += dp[j+1]
        return dp[0]
        
                
        
        
        
        
        
        
        
    