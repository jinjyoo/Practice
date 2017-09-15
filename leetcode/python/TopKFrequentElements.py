# https://leetcode.com/problems/top-k-frequent-elements/description/

from collections import Counter
from collections import defaultdict
import itertools
import heapq

class Solution(object):
    def topKFrequent(self, nums, k):  #Assume NO tiebreakers, e.g. if k = 2, then there is a unique answer
        """
        :type nums: List[int]
        :type k: int
        :rtype: List[int]
        """
        # return self.solution1(nums, k)  # 89 ms, 21.01%
        # return self.solution2(nums, k)  # 82 ms, 28.07%
        # return self.solution3(nums, k)  # 92 ms, 18.10%
        return self.solution4(nums, k)  # 52 ms, 96.90%
    
    def solution1(self, nums, k):  # O(n log k) since most_common uses heap, but this is somewhat shady
        return [key for key, _ in Counter(nums).most_common(k)]
        # return zip(*collections.Counter(nums).most_common(k))[0]  # Alternative
    
    def solution2(self, nums, k):
        heap = [(val, key) for (key, val) in Counter(nums).iteritems()]  # make value the priority, which has to be first
        heapq.heapify(heap)
        return [key for _, key in heapq.nlargest(k, heap)]
        """Alternative""" # https://discuss.leetcode.com/topic/44323/1-line-python-solution-using-counter-with-explanation/6
        # num_count = collections.Counter(nums)
        # return heapq.nlargest(k, num_count, key=lambda k: num_count[k])
    
    # Bucket Sort, from: https://discuss.leetcode.com/topic/44237/java-o-n-solution-bucket-sort/3
    def solution3(self, nums, k):  
        bucket = [[] for _ in nums]
        for num, freq in collections.Counter(nums).iteritems():
            bucket[-freq].append(num)  # higher freq goes further left, and freq < len(bucket)
        return list(itertools.chain(*bucket))[:k]  # chain removes the empty buckets at beginning
    
    def solution4(self, nums, k):  # fastest solution
        freq_map = defaultdict(int)
        for n in nums:
            freq_map[n] += 1
        items = [(-freq, num) for num, freq in freq_map.iteritems()]
        heapq.heapify(items)
        return [heapq.heappop(items)[1] for _ in xrange(k)]
        