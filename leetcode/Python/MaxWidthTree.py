# https://leetcode.com/problems/maximum-width-of-binary-tree/description/

# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

"""
[]
[1]
[1,3,2,5,3,null,9]
[1, 3, null, 5, 3]
[1, 3, 2, 5]
[1,3,2,5, null,null,9,6,null,null,7]
"""
from collections import deque
class Solution(object):
    def widthOfBinaryTree(self, root):
        """
        :type root: TreeNode
        :rtype: int
        """
        # return self.attempt1(root)  # TLE
        return self.solution1(root)   # 45 ms, 89%

    def attempt1(self, root):   # TLE  
        res = 0
        queue = [root]
        while any(queue):
            res = max(res, self.get_width(queue))
            # queue = [kid for node in queue if node for kid in (node.left, node.right)]   # doesn't propogate None's "children"
            # queue = [kid if node else [None]*2 for node in queue for kid in (node.left, node.right)]  # doesn't work
            temp = []
            for node in queue:
                if node:
                    temp.extend([node.left, node.right])
                else:
                    temp.extend([None]*2)
            queue = temp
        return res
        
    def get_width(self, lst):  # lst is nonempty
        start, end = 0, len(lst)-1  # first/last not-None instances
        for i in xrange(len(lst)):
            if lst[i] is not None:
                start = i
                break
        for j in xrange(len(lst)-1, i-1, -1):  # need to include i, e.g. if there is 0-1 non-None elements
            if lst[j] is not None:
                end = j
                break
        # print "{} {} {}".format(lst, start, end)
        return end - start + 1
    
    
    def solution1(self, root):  # use heap indices   # 45 ms, 89%
        if not root:
            return 0
        res = 0
        queue = deque([(root, 0)])
        while queue:
            # start, end = -1, -1
            start, end = queue[0][1], queue[-1][1]
            for _ in xrange(len(queue)):
                node, idx = queue.popleft()
                # if node:   # For some reason this version didn't work; the new version is faster and cleaner, anyway, but check later.
                    # if start == -1: 
                    #     start = i
                    # end = i
                    # queue.extend([(node.left, 2*idx), (node.right, 2*idx + 1)])
                if node.left:
                    queue.append((node.left, 2*idx))
                if node.right:
                    queue.append((node.right, 2*idx + 1))              
            # if start != -1:  # not all None
            res = max(res, end - start + 1)
        return res
                    
            

            