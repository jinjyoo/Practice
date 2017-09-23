# https://leetcode.com/problems/132-pattern/description/

"""
[1,2,3,4]
[3, 1, 4, 2]
[-1, 3, 2, 0]
[3,5,0,3,4]
[18,20,14,16,10,12,6,8,2,4,19]
"""
# from collections import deque
class Solution(object):
    def find132pattern(self, nums):
        """
        :type nums: List[int]
        :rtype: bool
        
        Notes: we want a_i to be as low as possible, and a_j to be as high as possible.  However, we have to have a_i before a_j. Flow:
        (1) Just a_i is set. (a) If we find something higher than a_i, set as a_j; (b) if lower, then set as a_i.
        (2) a_i and a_j set. (a) If we find something higher than a_j, set as a_j; (b) if lower, then we check with a_i.
            If higher than a_i, we're done. If lower than a_i, we have to keep track of it as well.
        (3) a_i, a_j, a_i2 set.  (a) If something higher than a_j, then we can discard a_i and a_j, and use a_i2 and a_j2.  
            (b) If lower than a_j: if higher than a_i, then True. If lower than a_i2, replace a_i2.  If higher than a_i2, set as a_j2.
        (4) a_i, a_j, a_i2, a_j2.  We now have five intervals, for a_j > a_i > a_j2 > a_i2:
            (a) a_k > a_j: remove a_i and a_j, a_j2 = a_k.
            (b) a_k > a_i: return True
            (c) a_k > a_j2: a_j2 = a_k.
            (d) a_k > a_i2: return True
            (e) a_k < a_i2: a_k = a_i3.
        Other notes: If a_k is higher than the biggest a_j, it is not the start of a potential new [a_i, a_j] pair, because anything that 
        fell into that would also fall into the original, lower [a_k, a_j2] pair.  Thus, any new (a_i, a_j) pair we add will have a_j <=
        all previous a_i's.  In other words, the (a_i, a_j) pairs make a decreasing sequence:
        a_j1 > a_i1 >= a_j2 > a_i2 >= a_j3 > a_i3 >= ...
        
        Simpler problem: finding 1-2-3 pattern.  Starting from the right, we keep updating the biggest s3, s2 candidates and return True
        if we find some s1 that's smaller than the current s2 candidate.  
        """
        # return self.solution1(nums)  # 129 ms -> 10.30%
        # return self.solution2(nums)  # 65 ms -> 92.27%
        return self.test3(nums)
    
    def test3(self, nums):
        s2, s3 = float('-inf'), float('-inf')
        for s1 in reversed(nums):
            print s1, s2, s3
            if s1 < s3:
                return True
            else:  # s1 >= s3
                if s1 > s2:
                    s2, s3 = s1, s2
                elif s1 > s3:  # problem -> since s2 wasn't updated, s3 cannot be assigned s1 because s3 is supposed to be after s2
                    s3 = s1
        return False
    
    # See also: https://discuss.leetcode.com/topic/68242/java-solutions-from-o-n-3-to-o-n-for-132-pattern-updated-with-one-pass-slution
    # https://discuss.leetcode.com/topic/67881/single-pass-c-o-n-space-and-time-solution-8-lines-with-detailed-explanation  
    def solution2(self, nums):  # From the fastest solution; O(n) time 
        """
        Idea: once we have an s2, we want to maximize s3 (preserving s2 > s3) to maximize the chance of finding some s1 < s3.
        
        Why we need a stack: 
        Take [1, 2, 3, 4].  For Test3, printing s1, s2, s3, we get:
        (1) 4, -inf, -inf  -> s2 = 4, s3 = -inf
        (2) 3, 4, -inf -> s2 stays 4, BUT we can't set s3 to 3, because it comes before s2.  Thus, we have to store it in a temporary
            buffer, and we can only let it be an s3 candidate if s2 gets updated to a new value before the 3.  If s2 gets updated, it is
            always to the currently being checked element, so everything that was seen before on the right is fair game for s3 
            (in particular, s2's old value).  
        With solution2, using [6, 4, 2, 3, 5], and printing s1, s3, s2:
        (1) 5, -inf, []  -> s2 = [5], s3 = -inf  # need to initialize s2 before s3 can be considered
        (2) 3, -inf, [5] -> s2 = [5, 3], s3 = -inf
        (3) 2, -inf, [5, 3] -> s2 = [5, 3, 2], s3 = -inf  
            s3 continues to be uninitialized, since s3 will only get updated once s2 gets updated; s2 is still 4, and since then, hasn't
            been updated, aka there is no (s2, s3) pair s.t. s2 > s3 (aka so far it's a decreasing sequence)                            
        (4) 4, -inf, [5, 3, 2] -> s2 = [5, 4], s3 = 3  # can get rid of [3, 2] in stack, and set s3 to 3 
            Note that it would've been incorrect to set s3 to 4 here, even though it's less than the biggest s2 = 5; we consider the most 
            recent s2 cand. along with the biggest possible s3 that came after any s2 (which is why s3 was pulled from the stack records). 
        (5) 6, 3, [5, 4] -> s2 = [6], s3 = 5    
            s2 gets updated, and s3 can now take the old value of 5                                   
            
            *We need to keep lowering our s2 standards so that we can find something higher than s2[-1] to trigger s3
            [4, 2, 7, 8, 9, 10]
            s1 = 1, s2 = [10, 9, 8, 7], s3 = -inf  -->  s2 = [10, 9, 8, 7, 1], s3 = -inf  
            s1 = 4, s2 = [10, 9, 8, 7, 1], s3 = -inf --> s2 = [10, 9, 8, 7, 4], s3 = 2:  <- (4, 2) is the current (s2, s3) pair; and this
                    was only made possible because we had lowered s2 enough (down to 2) so that 4 would trigger and we'd get a valid 
                    (s2, s3) pair (if we had not accepted 2, then we'd have had to find something higher than 7).  We want s2 as high as 
                    possible, so we keept track of all the highest numbers in case we find some almost-as-high numbers later, but accept
                    low numbers so that we increase the chance of finding a higher number to define (s2, s3) in the first place.  
                    
                    *However, our standards lower only as far as s3; e.g. if s3 is 4, then s2 would not accept a value lower than 4 (e.g. 2)
                    because that would just mean that we could have pairs such as (3, 2), but since we already have (something, 4), we don't 
                    bother (technically, of course, if we found a 2, since 2 < s3 = 4, we'd be done).  At the start, s3 = -inf, so s2 will 
                    accept anything.  
                    
            [4, 1, 2, 7, 8, 9, 10]
            s1 = 4, s2 = [1, 2, 7, 8, 9, 10], s3 = -inf  -->  Here, we finally have a s2 > s3 pair.  We can choose either (4, 1) or (4, 2),
            and we choose to maximize s3 (since we need s1 < s3) so we choose (4, 2), even though (4, 1) is just as valid. 
            
            [3, {4, 1, 2, 7, 8, 9, 10}]
            s1 = 3, s2 = [10, 9, 8, 7, 4], s3 = 2  -->  s2 adds 3, s3 is unable to upgrade 
            
            [13, 7, 11, {3, 4, 1, 2, 7, 8, 9, 10}]
            We find a high number: s2 = [11], s3 = 10
            ^Every number in s2 is a number that so far does not have a bigger number before it; every number that gets popped off had a 
            number before it. Here, all of s2 -[10, 9, 8, 7, 4]- was popped off, so to all of them, 11 was the biggest number to their left.
            Thus (11, 10), (11, 9), etc. are all valid, and we choose (11, 10). 11 is the only number in the s2-stack, because currently
            it is the only number found thus far (starting from the right) that doesn't have a bigger number to its left.
            
            We see 7, and return: 7 < 10 < 11.  
            
        """
        s3 = float('-inf')  # s3 will store the lowest value found so far
        s2 = []             # stores numbers currently greater than s3, which are s2 AND s3 candidates; will be in decreasing order
                            # every number in s2 is a number that we have not found a bigger number to its left yet
        for s1 in reversed(nums):  # Is there any subsequence s.t. s1 = nums[i]?
            if s1 < s3:  # s1 < s3, and s3 could only be > float('-inf') if there was some s2 > s3, so we have the pattern
                return True
            # At this point, s1 >= s3
            while s2 and s1 > s2[-1]:  # we now have a (s2, s3) potential pair
                s3 = stack.pop()  # since s2 was in decreasing order, after the loop, everything in s2 is still bigger than s3
                        # everything smaller than s1 is now fair game for the (s2=s1, __) pair, so might as well grab the biggest possible
            s2.append(s1)  # since s1 >= s3, we have  s2[-1] >= s3 still.
                # We append even if s1 < s2[-1], because we need to lower our s2-standards to increase chance of getting an (s2, s3) pair,
                # making it easier to find a number bigger than our lowest s2 (then we raise our standards, minimum s3).
        return False
    
    def solution1(self, nums):  # Mostly same as attempt2, but changed order of processing -> O(n) time
        if len(nums) < 3:
            return False
        bounds = [(nums[0], nums[0])]
        for i in xrange(1, len(nums)):
            a_k = nums[i]
            if a_k < bounds[-1][0]:  # len(bounds) >= 1
                bounds.append((a_k, float("-inf"))) 
            elif a_k > bounds[0][1]:  # added: avoid running through all of bounds later
                bounds = [(bounds[-1][0], a_k)]  # smallest ever value with biggest ever value
            else:
                for a_i, a_j in reversed(bounds):   # need to reverse; could improve with binary search or something
                    if a_k < a_j:                 
                        if a_k > a_i:
                            return True
                        else:  # if a_k <= a_i, then we can't continue
                            break
                    # else: a_k >= a_j, so we need to check the next [a_i, a_j]
                a_i = bounds[-1][0]  
                while bounds and a_k >= bounds[-1][1]: 
                    bounds.pop()
                bounds.append([a_i, a_k])
        return False        
        

    def attempt2(self, nums):   # TLE, 94/95 tests passed.  O(n) average, but O(n^2) worst case (when nums is the decreasing pattern.)
        if len(nums) < 3:
            return False
        # bounds = deque([nums[0], float("-inf")])     
        bounds = [(nums[0], float("-inf"))]  # used to be list, for overwriting bound[1], but more general to just pop and push new range
        for i in xrange(1, len(nums)):       # ^Could use nums[0] instead of float("-inf")
            a_k = nums[i]
            for a_i, a_j in bounds:
                if a_i < a_k < a_j:
                    return True
            if a_k < bounds[-1][0]:  # len(bounds) >= 1
                bounds.append((a_k, float("-inf"))) 
            else:  
                a_i = bounds[-1][0]
                while bounds and a_k >= bounds[-1][1]:  # use == as well, since e.g. [4, 10] still should get replaced by [3, 10]
                    bounds.pop()
                bounds.append([a_i, a_k])
        return False        
        """^Since a_k didn't trigger True in first for-loop, it's either smaller than the smallest a_i, OR it's in the range 
        [a_j, prev(a_i)] for some a_j. E.g. [10, 15], [5, 8], [0, 2] -> somewhere in (2, 5) or (8, 10).  Note that if a_k is in (8, 10)
        - WLOG, say 9 - then we can remove [5, 8], because it's redundant with the new [0, 9]. In general, while a_k > a_j, we can pop
        every [a_i, a_j] off the stack and then push [first_a_i, a_k] onto the stack.
        """           
                
        
        
    def attempt1(self, nums):  # Didn't notice that the 132 pattern doesn't have to be contiguous, just need i < j < k
        if len(nums) < 3:
            return False
        # i = 0
        # try:
        #     while i < len(nums):
        #         # if nums[i] < nums[i+2] < nums[i+1]:
        #         if nums[i] < nums[i+2]:
        #             if nums[i+2] < nums[i+1]:
        #                 return True
        #             i += (nums[i+2] == nums[i+1])  # 133 -> i+2; else if 123/103 -> i+1
        #         i += 1    
        # except IndexError:
        #     return False
        # return True
                
                
        