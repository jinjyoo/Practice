# https://leetcode.com/problems/gas-station/description/

"""
[4]
[5]
[10, 8, 3, 1, 5, 3, 13]
[1, 3, 9, 8, 1, 13, 2]
[5]
[4]
"""

class Solution(object):
    """
    Notes: Solution is guaranteed to be unique, so no more than 1 gas station will let you complete a full circuit (if possible).
    There is (no more than) one starting index s.t. Diff[i] >= 0 for all i.
    Cannot just find greatest diff.  E.g.: G[10, 0, 5] and C[1, 11, 2] -> need to start at (5, 2), not (10, 1)
    Cannot just find biggest negative diff and save for last, nor can you find the biggest continuous negative diff.
    E.g.: D[9, 5, -6, -7, 4, -10, 11]  -> have to start at 11
    
    Clarifications not explicitly given: len(gas) == len(cost), don't need to check.
    If there is one station, you still need to travel around back to it.
    """
    def canCompleteCircuit(self, gas, cost):  # Do not know which gas station we'll be starting at
        """
        :type gas: List[int]
        :type cost: List[int]
        :rtype: int
        """
        # return self.solution1(gas, cost)  # 1505 ms -> 2.61%  
        # return self.solution2(gas, cost)  # 35 ms -> 80.22%
        return self.solution3(gas, cost)  # 32 ms -> 93.48%  
    
    def solution1(self, gas, cost):   # Naive O(n^2) time
        if not gas:
            return None
        n = len(gas)
        diff = [gas[i] - cost[i] for i in xrange(n)]  # gas you get at station i, minus gas it costs to get to station i+1
        diff.extend(diff)  # for ease of circular calculations; technically just needed diff[:-1], but probably slower
        # diff.extend(diff[i] for i in xrange(n-1))
        for i in xrange(n):
            idx = self.check(diff, i, n+i)
            if idx != -1:
                break
        return idx
        
    def check(self, diff, start, end):
        curr_gas = 0
        for i in xrange(start, end):
            curr_gas += diff[i]
            if curr_gas < 0:
                return -1
        return start
    
    def solution2(self, gas, cost):
        """
        Idea: The unique starting indexing is after the lowest point in the graph; min_val depends on start, but min_idx is constant, 
        Improvements: could make clearer by initializing min_idx to 0, and then setting to i+1 instead
        Proof of correctness:
        (1) Start at A; let B be the first station that can't be reached from A.  For every C en route to B, the gas coming in was >= 0.  
            Starting at C would leave you at 0 coming in, so no in-between city C will help.  Thus, we jump to B rather than A+1. 
            *Alt proof here: https://discuss.leetcode.com/topic/8860/fully-commented-o-n-c-solution-enabled-by-a-single-observation-of-mine
            ^Assume some in-between city C could reach B.  Then A could reach C, and C can reach B, so A can reach B -> contradiction.
        (2) WLOG, start at 0.  Let i be the lowest cumulative total; then we have to prove that i+1 is the starting point.  
            Since the min occurs with the sum diff[0] + ... + diff[i], we have diff[i+1] >= 0 (otherwise, i would not be min_idx)
            Similarly, diff[i+1] + diff[i+2] >= 0.  And diff[i+1] + ... + diff[n-1] >= 0 -> diff[j] >= 0 for all i in [i+1, n-1], so 
            i+1 is a valid starting point for the second half.  Let diff[i+1 -> n-1] = D.  Given that diff[0 -> n-1] >= 0, we have:
            D + diff[0->i] >= 0.  Since D is enough to compensate for diff[0->i] (the most negative cumulative sum starting from 0), 
            D is enough to compensate for any diff[0->j], j <= i.  In particular, D + diff[0] >= 0, D + diff[0] + diff[1] >= 0, etc., and
            so from i+1, we have curr_gas >= 0 for every step, and thus i+1 is always a valid starting point (the only one, in this case.)
            * See also: https://discuss.leetcode.com/topic/39755/proof-of-if-total-gas-is-greater-than-total-cost-there-is-a-solution-c
        """
        if not gas:
            return None
        min_idx = -1  ### changed to -1; doesn't matter if overwritten, but if not (curr_gas never went <= 0), will return 0 
        min_val = 0   # ^If curr gas never goes below 0 then all diffs are positive, which means n solutions; but by uniqueness, n = 1
        curr_gas = 0  # ^So this is purely to address the case of n = 1, with positive cost (e.g. [5] [4])
        for i in xrange(len(gas)):
            curr_gas += gas[i] - cost[i]
            if curr_gas < min_val:  ### changed to include equals, because if we get multiple flat, we want to get to last one
                min_val = curr_gas  # ^changed back to exclude, because flat just means no gain, but also no loss -> no problem
                min_idx = i    
        return min_idx+1 if curr_gas >= 0 else -1  # after min_idx, it must be flat or increasing, otherwise minimum would be elsewhere

    def solution3(self, gas, cost):  # Apparently sum is very fast, because despite 3 traversals as opposed to 1, it's faster than Sol2
        if len(gas) == 0 or len(cost) == 0 or sum(gas) < sum(cost):
            return -1 
        position = 0
        balance = 0
        for i in xrange(len(gas)):
            balance += gas[i] - cost[i]
            if balance < 0:
                balance = 0
                position = i + 1
        return position
    
    # From: https://discuss.leetcode.com/topic/5088/my-ac-is-o-1-space-o-n-running-time-solution-does-anybody-have-posted-this-solution
    def solution4(self, gas, cost):
        start, end = len(gas)-1, 0  # we're arbitrarily starting on the "last" gas station
        curr_gas = gas[start] - cost[start]
        while start > end:
            if curr_gas >= 0:
                curr_gas += gas[end] - cost[end]  # we can keep driving
                end += 1
            else:
                start -= 1  # we can't keep going with the gas have, so we have to have started earlier to build up stock
                curr_gas += gas[start] - cost[start]
        return start if curr_gas >= 0 else -1
    
        """For reference: old work that was eventually discarded for Solution2, but which would eventually have reached solution4"""
        # start = n  # diff has been doubled 
        # curr_gas = 0
        # for i in xrange(start, len(diff)):  
        #     curr_gas += diff[i]
        #     if curr_gas < 0:
        #         offset = i - start  # [start, i-1] is good    
        #         while curr_gas < 0: # starting from diff[i] is no longer possible, so we need to build up stock by starting earlier     
            
        