# https://leetcode.com/problems/populating-next-right-pointers-in-each-node/description/

# Definition for binary tree with next pointer.
# class TreeLinkNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None
#         self.next = None

# Need constant space, so can't make heap, and can't use recursion
class Solution:
    # @param root, a tree link node
    # @return nothing
    def connect(self, root):
        # return self.solution1(root)   # 85 ms, 52%
        return self.solution2(root)     # 82 ms, 58%
    
    def solution1(self, root):  # 85 ms, 52%
        if not root: 
            return 
        root.next = None
        num_parents = 1
        node = root
        left_child, right_child = node.left, node.right
        while left_child:
            first_left_child = left_child
            for _ in xrange(num_parents-1):  # all except for on right-most node, we need to set to None
                left_child.next = right_child
                node = node.next            # Key insight - we can use the result of previous work
                left_child = node.left
                right_child.next = left_child
                right_child = node.right
            left_child.next = right_child
            right_child.next = None
            
            node = first_left_child
            left_child, right_child = node.left, node.right
            num_parents *= 2  # not +1

    # We can save time by noting we don't have to explicitly set the last node.next to None
    # Cleaner to not have variables for left_child, right_child
    def solution2(self, root):  # https://discuss.leetcode.com/topic/16547/7-lines-iterative-real-o-1-space
        while root and root.left:
            next = root.left
            while root:
                root.left.next = root.right
                root.right.next = root.next and root.next.left  # a if False else b; somewhat dangerous
                root = root.next
            root = next
            
    def solution3(self, root):  # https://discuss.leetcode.com/topic/2202/a-simple-accepted-solution  (C++) 
        if root: 
            while root.left:
                cur = root
                while cur:
                    cur.left.next = cur.right
                    if cur.next: 
                        cur.right.next = cur.next.left
                    cur = cur.next
                root = root.next 
        
        
        
         