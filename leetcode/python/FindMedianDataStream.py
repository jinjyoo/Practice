# https://leetcode.com/problems/find-median-from-data-stream/description/

"""
Other solutions:
https://discuss.leetcode.com/topic/30495/tired-of-two-heap-set-solutions-see-this-segment-dividing-solution-c  (Sort just a bucket)
https://stackoverflow.com/questions/10657503/find-running-median-from-a-stream-of-integers/10693752#10693752  (Approx. only, Reserv. Samp.)
"""
import heapq
class Solution2(object):  # Modified from fastest solution

    """
    Shorter versions:
    https://discuss.leetcode.com/topic/27521/short-simple-java-c-python-o-log-n-o-1
    https://discuss.leetcode.com/topic/27541/very-short-o-log-n-o-1
    https://discuss.leetcode.com/topic/27522/java-python-two-heap-solution-o-log-n-add-o-1-find
    """
    def __init__(self):
        self.smaller = []  # max_heap of smaller half of numbers
        self.larger = []  
        
    def addNum(self, num):
        """
        This time, either smaller/larger can have more elements (by no more than one), which means less push/pop so that min is >= max
        """
        num = float(num)  # not really necessary, it means everything in heap is float 
        if not self.smaller or num <= -self.smaller[0]:
            heapq.heappush(self.smaller, -num)
        else:
            heapq.heappush(self.larger, num)            
        if len(self.smaller) - len(self.larger) > 1:
            heapq.heappush(self.larger, -heapq.heappop(self.smaller))
        if len(self.larger) - len(self.smaller) > 1:
            heapq.heappush(self.smaller, -heapq.heappop(self.larger))

    def findMedian(self):
        if not self.smaller and not self.larger:
            return 0
        if len(self.smaller) == len(self.larger):
            return (self.larger[0] - self.smaller[0]) / 2.0
        elif len(self.smaller) > len(self.larger):
            return -self.smaller[0]
        else:
            return self.larger[0]

import heapq
class Solution1(object):  # Probably could make less janky with separate max_heap class

    def __init__(self):
        """Sort of like sliding window of 2."""
        self.hmin = []  # Store the half of the stream with bigger numbers
        self.hmax = []  # Store the half of the stream with smaller numbers

    def addNum(self, num):
        """
        Favors hmin, so (1) len(hmin) >= len(hmax)
        Other invariants: (2) hmax[0] <= hmin[0], (3) 0 <= len(hmin) - len(hmax) <= 1     
        """
        try:
            if num < -self.hmax[0]:  # has to go on hmax
                if len(self.hmax) == len(self.hmin):
                    heapq.heappush(self.hmin, -heapq.heappop(self.hmax))
                heapq.heappush(self.hmax, -num)
            elif num > self.hmin[0]:
                if len(self.hmin) > len(self.hmax):
                    heapq.heappush(self.hmax, -heapq.heappop(self.hmin))
                heapq.heappush(self.hmin, num)
            else: # hmax[0] <= num <= hmin[0]
                if len(self.hmin) > len(self.hmax):
                    heapq.heappush(self.hmax, -num)
                else:
                    heapq.heappush(self.hmin, num)
        except IndexError:  # Couldn't think of a more elegant way of doing this besides if-check, which would only occurs twice 
            if not self.hmin:
                heapq.heappush(self.hmin, num)
            else: 
                if num > self.hmin[0]:
                    heapq.heappush(self.hmax, -heapq.heappop(self.hmin))
                    heapq.heappush(self.hmin, num)
                else:
                    heapq.heappush(self.hmax, -num)
        # print 'After:', num, list(reversed(self.hmin)), self.hmax

    def findMedian(self):
        if len(self.hmin) != len(self.hmax):  # odd number
            return self.hmin[0]  # hmin has more
        else:
            return (self.hmin[0] - self.hmax[0]) / 2.0
        
# MedianFinder = Solution1  # 372 ms -> 89.77%
MedianFinder = Solution2  # 325 ms -> 98.72%

# Your MedianFinder object will be instantiated and called as such:
# obj = MedianFinder()
# obj.addNum(num)
# param_2 = obj.findMedian()