# https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/description/

# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None
"""
Tests:
[]
[]
[1, 2, 4, 5, 3, 6]
[4, 2, 5, 1, 6, 3]
[1]
[1]
[1, 2, 3, 4, 5]
[2, 4, 5, 3, 1]
[1, 2, 4, 3, 5, 6, 7]
[2, 4, 1, 3, 6, 5, 7]
"""
from collections import deque

class Solution(object):
    def buildTree(self, preorder, inorder):
        """
        :type preorder: List[int]  # Not like typical input, so no 'None'
        :type inorder: List[int]
        :rtype: TreeNode
        """
        # return self.solution1(preorder, inorder)  # 259 ms -> 51%; O(n^2) worst case
        return self.solution2(preorder, inorder)    # 59 ms -> 95%

    # If tree is straight line to the left, then pre/in are reversed and searching for r_idx will be O(n) every time -> O(n^2)
    """Fix: Save space by thinking of children as just nodes, a la recursion"""
    def solution1(self, preorder, inorder):  # 259 ms -> 51%
        if not preorder:  # technically covered by "if not inorder" for first iteration
            return None
        return self.helper(deque(preorder), inorder)  
    
    def helper(self, preorder, inorder):  
        if not inorder:  
            return None
        root = TreeNode(preorder.popleft())  
        r_idx = inorder.index(root.val);  # could optimize by building dict over inorder - stopping values
        left_children, right_children = inorder[:r_idx], inorder[r_idx + 1:]  # splitting also costs O(k), could use indices instead
        if left_children:
            if len(left_children) == 1:
                root.left = TreeNode(left_children[0])
                preorder.popleft()  # kinda janky...
            else:
                root.left = self.helper(preorder, left_children)
        if right_children:
            if len(right_children) == 1:
                root.right = TreeNode(right_children[0])
                preorder.popleft()
            else:
                root.right = self.helper(preorder, right_children)
        return root                
        
    # https://discuss.leetcode.com/topic/16221/simple-o-n-without-map?show=44432   # O(n) time, O(1) space
    def solution2(self, preorder, inorder): # 59 ms -> 95%
        def build(stop):
            if inorder and inorder[-1] != stop:  # not the root value
                root = TreeNode(preorder.pop())
                root.left = build(root.val)
                inorder.pop()
                root.right = build(stop)
                return root
        preorder.reverse()
        inorder.reverse()
        return build(None)

    # https://discuss.leetcode.com/topic/41050/compact-python-solution-beats-88
    def solution3(self, preorder, inorder):  # O(n) time, O(n) space; more intuitive than solution2
        self.preorder = preorder
        self.itable = {v:i for i, v in enumerate(inorder)}
        return self.helper3(0, 0, len(preorder))

    def helper3(self, pbegin, ibegin, size):  # len (preorder)
        if not size: return None
        root = TreeNode(self.preorder[pbegin])
        stop = self.itable[root.val]
        lsize = stop - ibegin       # [ibegin, stop)
        rsize = size - lsize - 1    # (stop, len(preorder)-1]
        root.left  = self.helper3(pbegin + 1,         ibegin,   lsize)
        root.right = self.helper3(pbegin + 1 + lsize, stop + 1, rsize)
        return root
        
    # https://discuss.leetcode.com/topic/35826/python-recursion-version-and-iteration-version-easy-to-understand
    # https://discuss.leetcode.com/topic/795/the-iterative-solution-is-easier-than-you-think
    def solution4(self, preorder, inorder):  # TODO - Iterative
        pass 

            
        