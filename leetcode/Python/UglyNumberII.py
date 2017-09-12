# https://leetcode.com/problems/ugly-number-ii/description/

class Solution(object):
    def nthUglyNumber(self, n):
        """
        :type n: int
        :rtype: int
        """
        # return self.solution1(n) # 172 ms
        return self.solution2(n)   # 49 ms
    
    # Similar: https://discuss.leetcode.com/topic/21882/my-16ms-c-dp-solution-with-short-explanation
    def solution1(self, n): # O(n) space/time, 172 ms    
        p2, p3, p5 = 0, 0, 0   # p2 stores last ugly number that was reached by multiplying 2
        dp = [0]*n  
        dp[0] = 1
        for i in xrange(1, n):
            a2, a3, a5 = dp[p2]*2, dp[p3]*3, dp[p5]*5  # See also: heap solution, easier to think about 
            ugly = min(a2, a3, a5)
            if a2 == ugly: p2 += 1
            if a3 == ugly: p3 += 1
            if a5 == ugly: p5 += 1
            dp[i] = ugly
        return dp[n-1]
    
    
    # From: https://discuss.leetcode.com/topic/21795/short-and-o-n-python-and-c/11 
    ugly = sorted(2**a * 3**b * 5**c for a in xrange(32) for b in xrange(20) for c in xrange(14))  # Precomputed once, magic numbers
    # ugly = sorted(for a, b, c in itertools.product(range(31), repeat=3)).
    def solution2(self, n):  # 49 ms  # Wasteful if not used called multiple times
        return self.ugly[n-1]  # only works because we know how far up to compute
