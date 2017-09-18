# https://leetcode.com/problems/design-twitter/description/

"""
["Twitter","postTweet","getNewsFeed","follow","postTweet","getNewsFeed","unfollow","getNewsFeed"]
[[],[1,5],[1],[1,2],[2,6],[1],[1,2],[1]]
["Twitter","postTweet","postTweet","postTweet","postTweet","postTweet","postTweet","postTweet","postTweet","postTweet","postTweet","getNewsFeed","follow","getNewsFeed"]
[[],[2,5],[1,3],[1,101],[2,13],[2,10],[1,2],[2,94],[2,505],[1,333],[1,22],[2],[2,1],[2]]
"""

from collections import defaultdict, deque
import heapq
import itertools as it

class Solution2(object):  # From: https://discuss.leetcode.com/topic/47838/python-solution

    def __init__(self):
        self.timer = it.count(step=-1)
        self.tweets = defaultdict(deque)
        self.followees = defaultdict(set)

    def postTweet(self, userId, tweetId):
        self.tweets[userId].appendleft((next(self.timer), tweetId))

    def getNewsFeed(self, userId):
        tweets = heapq.merge(*(self.tweets[u] for u in self.followees[userId] | {userId}))
        return [t for _, t in it.islice(tweets, 10)]

    def follow(self, followerId, followeeId):
        self.followees[followerId].add(followeeId)

    def unfollow(self, followerId, followeeId):
        self.followees[followerId].discard(followeeId)

class Solution1(object):  
    """
    Notes:
    Feed includes your own tweets; LIFO, use stack/deque.  
    Should give each tweet its own tweet id, since the feed returns the 10 most recent things.
    Followers-Following: Sparse graph, so use something like an adjacency list, using dictionaries for fast lookup.
    
    Main problems: 
    (1) How to get the feed?  Somewhat inefficient to parse all the people you're following. Maybe have the followers push to all following? 
        But this would be extra unnecessary work if the person is unfollowed, unlike if the feed is generated on-demand only.
    (2) If you unfollow, that will affect the feed.  We'd end up needing a full history even though not explicitly required, since e.g.
        feed consists entirely of tweets from Followed-A.  Unfollow -> Need to pull ten tweets before that, possibly have to repeat.
        Conclusion: Instead of storing entire history, should probably just do on-demand.
        This means people have to know who they're following.  Followers do not have to know who is following them.
    """

    def __init__(self):
        """Notes: No separate list of users.  Everyone always follows at least one person, themself (and cannot unfollow themselves)"""
        self.following = defaultdict(set)  # person: set(following)
        self.tweets = defaultdict(deque)  # person: stack(tweets); deque used for heapq, since Python2 heapq doesn't have reversed (P3 does)
        self.time_stamp = 0  # cannot assume tweetIds provided will be unique or in increasing order

    def postTweet(self, userId, tweetId):  
        self.tweets[userId].appendleft((self.time_stamp, tweetId))  # Use negative for maxHeap
        self.following[userId].add(userId)    # somewhat inefficient?
        self.time_stamp -= 1

    def getNewsFeed(self, userId):
        pool = self.following[userId]  # get list of all followers 
        feed = heapq.merge(*[self.tweets[fid] for fid in self.following[userId]])  # all tweets should be sorted already
        return [item[1] for item in it.islice(feed, 10)]  
        # return list(it.islice(feed, 10))

    def follow(self, followerId, followeeId):
        # if followeeId in self.users:   # check if followeeId is valid?  But we don't know who the valid users are.
        self.following[followerId].add(followeeId)  

    def unfollow(self, followerId, followeeId):
        if followerId != followeeId and followerId in self.following:  # defaultdicts still error if deleting with nonexistent key
            self.following[followerId].discard(followeeId)  # unlike remove, discard doesn't error if followeeId doesn't exist
        
# Alias for multiple solutions  
# Twitter = Solution1  # 108 ms, 65.09%
Twitter = Solution2  # 92 ms, 93.97%

# Your Twitter object will be instantiated and called as such:
# obj = Twitter()
# obj.postTweet(userId,tweetId)
# param_2 = obj.getNewsFeed(userId)
# obj.follow(followerId,followeeId)
# obj.unfollow(followerId,followeeId)