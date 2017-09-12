# https://leetcode.com/problems/minimum-path-sum/description/

"""
[[]]
[[0]]
[[1]]  # cache pitfall
[[1, 3, 2, 7, 6], [4, 8, 5, 9, 7], [3, 9, 2, 7, 5]]
"""
import functools 
def memo(func): # Problem: only one copy of cache, need to tie to self
    cache = {}  # grid is not hashable, so we can't pass it in
    @functools.wraps(func)
    def decorated_function(self, *args):  # self is defined at runtime
        if args not in cache:  
            cache[args] = func(self, *args)  # cannot do self.func, because then Solution looks for a function called func
        return cache[args]
    return decorated_function

class Memoize:  # From: https://www.python-course.eu/python3_memoization.php
    def __init__(self, fn):
        self.fn = fn
        self.memo = {}
    def __call__(self, *args):
        if args not in self.memo:
	    self.memo[args] = self.fn(*args)
        return self.memo[args]

class Solution(object):
    def minPathSum(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """
        # return self.solution1(grid)  # 69 ms, 31%  - Bottom-Up Recursion
        # return self.solution2(grid)  # 55 ms, 74% - Rolling Array, Bottom-Up Recursion
        # return self.solution3(grid)  # 112 ms, 10% - Top-Down
        return self.solution4(grid)    # Top-Down with wrappers
    
    def solution1(self, grid):   # O(mn) time, O(mn) space
        if not grid or not grid[0]: 
            return 0
        # dp = [row[:] for row in grid]  # to initialize first row and col -> base cases
        m, n = len(grid), len(grid[0])
        dp = [[0]*n for _ in xrange(m)]
        dp[0][0] = grid[0][0]
        for i in xrange(1, m):
            dp[i][0] = grid[i][0] + dp[i-1][0]
        for j in xrange(1, n):
            dp[0][j] = grid[0][j] + dp[0][j-1]
        for i in xrange(1, m):
            for j in xrange(1, n):
                dp[i][j] = grid[i][j] + min(dp[i][j-1], dp[i-1][j])  # we can only move down or right, so only have to check up/left
        return dp[m-1][n-1]  
    
    def solution2(self, grid):  #O(mn) time, O(n) space
        if not grid or not grid[0]:
            return 0
        m, n = len(grid), len(grid[0])
        dp = [0]*n
        dp[0] = grid[0][0]
        for i in xrange(1, n):
            dp[i] = dp[i-1] + grid[0][i]
        for i in xrange(1, m):
            for j in xrange(n):  # don't have to do backwards; must start at 0
                dp[j] = grid[i][j] + min(dp[j], dp[j-1])
        return dp[n-1]

    def solution3(self, grid):  #O(mn) time, O(mn) space
        if not grid or not grid[0]:
            return 0
        self.grid = grid  # need for memo because grid is not hashable
        self.cache = {}   # memo didn't work, need fresh cache for every grid
        m, n = len(grid), len(grid[0])
        return self.helper(m-1, n-1)
        
    def helper(self, i, j):
        if (i, j) not in self.cache:
            if i == 0:
                self.cache[(i, j)] = self.grid[0][j] + self.helper(0, j-1) if j != 0 else self.grid[0][0]  # clearer than grid[i][j]
            elif j == 0:
                self.cache[(i, j)] = self.grid[i][0] + self.helper(i-1, 0)
            else: 
                self.cache[(i, j)] = self.grid[i][j] + min(self.helper(i-1, j), self.helper(i, j-1))
        return self.cache[(i, j)]
           
    def solution4(self, grid):
        if not grid or not grid[0]:
            return 0
        self.grid = grid
        m, n = len(grid), len(grid[0])
        return self.helper(m-1, n-1)
        
    # @memo    # cannot do because memo outside Solution creates one cache; grid is the key but it isn't hashable
    # @self.memo   # cannot put memo inside Solution because self does not exist; we're outside any function. cls is same prob as above.
    @Memoize
    def helper(self, i, j):
        if i == 0:
            return self.grid[0][j] + self.helper(0, j-1) if j != 0 else self.grid[0][0]  # clearer than grid[i][j]
        if j == 0:
            return self.grid[i][0] + self.helper(i-1, 0)
        return self.grid[i][j] + min(self.helper(i-1, j), self.helper(i, j-1))

        
        