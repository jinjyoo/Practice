# https://leetcode.com/problems/2-keys-keyboard/description/
"""
1
3
8
9
12
20
997
999
1000
"""

class Solution(object):

    def minSteps(self, n):  # Assume n >= 1
        """
        :type n: int
        :rtype: int
        """
        # return self.solution1(n)  # 36 ms, 80.91%  
        return self.solution2(n)  # 33 ms, 91.22%  # Sol 2/3 are probably the best (basically the same)
        # return self.solution3(n)  # 35 ms, 85.04%
        # return self.solution4(n)  # 695 ms, 29.21%
        # return self.solution5(n)  # 36 ms, 80.91%
        
    def solution1(self, n):   # 36 ms, 80.91%.  O(n) worst case on primes, O(log n) average case.
        """Observations:
        Except for n = 1, everything must start with a C, P.
        Invariants: p_len <= n/2.  
                    rem % p_len == 0 
                    p_len_old <= p_len_new/2  (not ==, since we could paste multiple times with p_len_old)
        Be greedy. C-P is two operations, but no worse than P-P, because of the third invariant; so always copy if new p_len is valid.
        """
        if n == 1:
            return 0
        res = 2       # C, P must always be done
        length = 2    # length of current string; always starts as 'AA'
        rem = n-length     # remainder
        p_len = 1     # paste length
        just_copied = False  # to avoid infinite loops
        while length < rem:  # While copying is still theoretically possible
            if not just_copied and (rem - length) % length == 0:  # latter more likely to be false, but avoid costly calculations
                # if (rem - length) % length == 0:  # this created an infinite loop
                p_len = length  # copy
                just_copied = True    
            else:
                rem -= p_len    # paste
                length += p_len
                just_copied = False  # Very important...
            res += 1
        return res + rem / p_len   
        
    # From: https://discuss.leetcode.com/topic/97623/loop-best-case-log-n-no-dp-no-extra-space-no-recursion-with-explanation
    def solution2(self, n):    
        res = 0  # e.g. 12 -> 2, 2, 3: 2 ops to get 2 (CP), 2 ops to get 4 (CP), 3 ops to get 12 (CPP)
        d = 2
        while d <= n:
            while n % d == 0:
                res += d  # it takes d steps to have d copies of (n/d)*'A': 1 step of Copy and (d-1) steps of paste (add d-1 of n/d)
                n /= d    # e.g. 15 in 15 operations (1 copy, 14 paste).  Can do 3 ops (CPP) then 5 ops (CPPPP) to get 3 + 4*3 = 15 copies
                          # equivalent to 5 ops (CPPPP) then 3 ops (CPP)
            d += 1
        return res
    
    # From: https://discuss.leetcode.com/topic/97618/python-straightforward-with-explanation
    def solution3(self, n):  
        def factors(n):
            d = 2
            while d * d <= n:
                while n % d == 0:
                    n /= d
                    yield d
                d += 1
            if n > 1:
                yield n
        return sum(factors(n))
    
    # From: https://discuss.leetcode.com/topic/97590/java-dp-solution
    def solution4(self, n):  # Pure DP, but slow because it doesn't cut down once maximum paste size is found
        dp = [0]*(n+1)
        for i in xrange(2, n + 1):
            dp[i] = i
            for j in xrange(i-1, 0, -1):  # while j > 1
                if i % j == 0:
                    dp[i] = dp[j] + (i / j)
                    break
        return dp[-1]
    
    # From: https://discuss.leetcode.com/topic/97629/python-code-beats-100
    def solution5(self, n):
        """This is essentially factorization of a integer, you find all its factors, and add them together."""
        if n == 1:
            return 0
        f = 1
        for i in xrange(int(n**0.5), 0, -1):
            if n%i == 0:
                f = i
                break
        if f == 1:
            return n
        return self.minSteps(f) + self.minSteps(n/f)

        