# https://leetcode.com/problems/unique-paths-ii/description/

"""
[[0]]
[[0,0,0],[0,1,0],[0,0,0]]
[[0,1,1],[0,1,0],[0,0,0]]
[[1,0,0],[0,1,0],[0,0,0]]
[[0,0,0],[0,1,0],[0,0,1]]
[[0,1],[0,0]]
[[0,0],[0,0]]
"""

class Solution(object):
    def uniquePathsWithObstacles(self, obstacleGrid):
        """
        :type obstacleGrid: List[List[int]]
        :rtype: int
        """
        # return self.solution1(obstacleGrid)  # 39 ms -> 50.79%
        # return self.solution2(obstacleGrid)  # 35 ms -> 80.74%
        return self.solution3(obstacleGrid)
    
    def solution1(self, obstacleGrid):
        if not any(obstacleGrid) or obstacleGrid[-1][-1] == 1 or obstacleGrid[0][0] == 1:
            return 0
        m, n = len(obstacleGrid)-1, len(obstacleGrid[0])-1  # number of D's and R's we have left
        if m == 0 or n == 0:
            return 1
        dp = [[0]*(n+1) for _ in xrange(m+1)]
        # dp[-1][-1] = 1
        for j in xrange(n, -1, -1):  # initialize last row
            if obstacleGrid[-1][j] == 1:
                dp[-1][:j+1] = [0]*(j+1)
                break
            dp[-1][j] = 1
        for i in xrange(m-1, -1, -1):
            if obstacleGrid[i][-1] == 1:
                for j in xrange(i+1):
                    dp[j][-1] = 0
                break
            dp[i][-1] = 1
        for i in xrange(m-1, -1, -1):
            for j in xrange(n-1, -1, -1):
                if obstacleGrid[i][j] == 1:
                    dp[i][j] = 0
                else:
                    dp[i][j] = dp[i+1][j] + dp[i][j+1]
        return dp[0][0]
     
    def solution2(self, obstacleGrid): 
        if not any(obstacleGrid) or obstacleGrid[-1][-1] == 1 or obstacleGrid[0][0] == 1:
            return 0
        m, n = len(obstacleGrid)-1, len(obstacleGrid[0])-1  # number of D's and R's we have left
        if m == 0 or n == 0:
            return 1    
        dp = [0]*(n+1)
        for j in xrange(n, -1, -1):  # initialize last row
            if obstacleGrid[-1][j] == 1:
                dp[:j+1] = [0]*(j+1)
                break
            dp[j] = 1
        for i in xrange(m-1, -1, -1):
            for j in xrange(n, -1, -1):  # changed from n-1, we can't ignore last column
                if obstacleGrid[i][j] == 1:
                    dp[j] = 0
                else:
                    if j < n:  # Ugly; could check dp[-1] before j-loop, but that'd introduce redundant logic
                        dp[j] += dp[j+1]  
        return dp[0]  
    
    def solution3(self, obstacleGrid): 
        """Can ignore initialization and keep same speed.  
        Java: https://discuss.leetcode.com/topic/10974/short-java-solution"""
        if not any(obstacleGrid) or obstacleGrid[-1][-1] == 1 or obstacleGrid[0][0] == 1:
            return 0
        m, n = len(obstacleGrid)-1, len(obstacleGrid[0])-1  # number of D's and R's we have left
        if m == 0 or n == 0:
            return 1    
        dp = [0]*(n+1)
        dp[-1] = 1
        for row in reversed(obstacleGrid):
            for j in xrange(n, -1, -1):  # changed from n-1, we can't ignore last column
                if row[j] == 1:
                    dp[j] = 0
                elif j < n:  # Ugly; could check dp[-1] before j-loop, but that'd introduce redundant logic
                    dp[j] += dp[j+1] 
        return dp[0]       
        
        