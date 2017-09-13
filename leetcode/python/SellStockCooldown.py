# https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/description/

"""
[1, 2]
[1,2,4]
[1,4,2]
[1,2,3,0,2]
[0, 10, 20, 10, 100]
[5, 4, 3, 2, 1]
"""

class Solution(object):
    """
    Kind of like House Robbers, except we have to worry about buying before each sale.
    """
    def maxProfit(self, prices):
        """
        :type prices: List[int]
        :rtype: int
        """
        # return self.practice(prices)
        # return self.attempt1(prices)
        # return self.solution1(prices)
        return self.solution2(prices)
    

    def solution1(self, prices):  # 48 ms, 34%
        """
        From: https://discuss.leetcode.com/topic/30421/share-my-thinking-process
        Clearer method: https://discuss.leetcode.com/topic/30431/easiest-java-solution-with-explanations (Solution 2)
        See also: https://discuss.leetcode.com/topic/30680/share-my-dp-solution-by-state-machine-thinking
        """
        if len(prices) < 2:
            return 0
        sell, buy, prev_sell, prev_buy = 0, -prices[0], 0, 0
        for price in prices:
            prev_buy = buy
            buy = max(prev_buy, prev_sell - price)
            prev_sell = sell
            sell = max(prev_sell, prev_buy + price)
        return sell
        
    def solution2(self, prices): # https://discuss.leetcode.com/topic/30431/easiest-java-solution-with-explanations
        if len(prices) < 2:
            return 0
        b1 = -prices[0]
        s1 = s2 = 0
        for i in xrange(1, len(prices)):
            b0 = max(b1, s2 - prices[i])
            s0 = max(s1, b1 + prices[i])
            s2, s1 = s1, s0
            b1 = b0
        return s0
        
    
    def attempt1(self, prices):  # O(n^2)  # Can't figure out indices, getting too complicated and messy anyway
        if len(prices) < 2:
            return 0
        dp = [0]*(len(prices)+2)    # want to be able to do a[i] - a[0] + dp[-2]; dp[i] is max_profit with first (i-1) items in price
        # print "i, j, prices[i-2], prices[(i-2)-j], dp[(i-3)-j], dp[i]"
        for i in xrange(3, len(prices)+2):
            dp[i] = max(0, *(prices[i-2] - prices[(i-2)-j] + dp[(i-3)-j] for j in xrange(1, i-1)))  # dp[(i-1)-j] for no cooldown
            # curr_max = 0
            # for j in xrange(1, i-1):
            #     print "{:<2} {:<2} {:<4} {:<3} {:<3} {:<3}".format(i, j, prices[i-2], prices[(i-2)-j], dp[(i-3)-j], dp[i])
            #     ans = prices[i-2] - prices[(i-2)-j] + dp[(i-3)-j]
            #     if ans > curr_max:
            #         print ans, i, j
            #         curr_max = ans
            # dp[i] = curr_max
        # print dp
        return dp[-1]    

        