# https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/description/

class Solution(object):
    def maxProfit(self, prices):
        """
        :type prices: List[int]
        :rtype: int
        """
        return self.solution1(prices)  # 46 ms, 37.4%
        return self.solution2(prices)  # 45 ms, 42.9%
    
    def solution1(self, prices):  # 46 ms, 37.4%; adopted from stock-with-cooldown
        if len(prices) < 2:
            return 0
        b0 = prices[0]; b1 = -prices[0]
        s0 = s1 = 0
        for i in xrange(1, len(prices)):
            b0 = max(b1, s1 - prices[i])
            s0 = max(b1 + prices[i], s1)
            s1 = s0
            b1 = b0
        return s0
    
    # Greedy algorithm, where we just get every positive change.  Note that we can't buy/sell on same day, 
    # but e.g. [1, 3, 5] would return 1->3, 3->5, which is equivalent to 1->5.  
    # See also: https://discuss.leetcode.com/topic/726/is-this-question-a-joke/14
    def solution2(self, prices):   
        # if len(prices) < 2:  # not necessary
        profit = 0
        for i in xrange(1, len(prices)):  
            if prices[i-1] < prices[i]:
                profit += prices[i] - prices[i-1]
            # diff = prices[i] - prices[i-1]
            # if diff > 0:
            #     profit += diff
        return profit
    
    def solution3(self, prices):  # https://discuss.leetcode.com/topic/27394/clear-1-line-python-solution
        return sum(max(prices[i + 1] - prices[i], 0) for i in xrange(len(prices)-1))
            
            