`num` = str(num) = repr(k)  # use repr for string conversion, much better and in Python3 as well
(a > b) - (a < b) => cmp(a, 0)  
s = cmp(x, 0)
r = int(`s*x`[::-1])
return s*r * (r < 2**31)

 L = [[0 for x in xrange(n+1)] for x in xrange(m+1)]  # j then i
  return ' '.join([str(i) for i in lcs])
n, m = map(int, raw_input().strip().split(' '))
p = map(int, raw_input().strip().split(' '))
left <= root.val <= 
get(key[, default])
len(your_list) != len(set(your_list))  # check for duplicates in a flat list
float.is_integer(); float('-inf'); 
sys.maxint #sys.maxsize for Python3, 2^31-1; sys.minsize = -2^31-1
sys.float_info[.max]  
#integers use C's long (32 bits); floats use C's double; 
#<number>L : long ints have no limit on bits (arbitrary precision, only limited by memory) -> Java's BigInteger

"""bits"""
# In two's complement system -x is the same as ~x+1
int('0b1011000', 2)
bin(), hex()
n&(n-1)  #flips least significant bit in n to 0
math.log(num, 3)
return (n > 0) and (n & (n-1)) == 0  # powers of 2
return num > 0 and (num&(num-1)) == 0 and (num & 0x55555555) != 0;  # 0b0101010101....01  # powers of 4


queue = deque([(root, 1)])  # need the brackets the first time, but not for append

"""WARNINGS"""
1 or 3 -> 1   # x or y: if x if False then y, else x
1 and 3 -> 3  # x and y: if x is False, then x, else y
not 1 -> False	# if x if False, then True, else False
6/2 = 3.0 (float)

for _ in range(d - 1):
        row = [kid for node in row for kid in (node.left, node.right) if kid]
        # row = [kid for kid in (node.left, node.right) if kid for node in row]
node.left, node.left.left = TreeNode(v), node.left
"""Lists - like Stacks
del a[0], a.remove(3) # first instance of 3


""" 
# ''.join(c for c in text if c.isupper())    # get upper case
# ''.join(filter(str.isupper, text))

# import unittest
# class MyTest(unittest.TestCase):
#     def test(self):
#         self.assertEqual(fun(3), 4)

Trie.Node()



"""Trees"""
if (not p) and (not q): return True
if (not p) or (not q): return False

"""
Binary Tree (and BSTs) - assume no duplicates

***DFS***
Inorder - in a search tree, retrieves data in sorted order
Preorder - used to create a copy of a tree (insert as nodes into array); the order for DFS
		also used to get prefix expression of an expression tree
		^Polish notation - places operator to left of operands (+ 5 3)
Postorder - reverse Polish notation (postfix), deleting a tree; reverse DFS (the order in which *last* visited)

Preorder - will encounter root before leaves
Postorder - for inspecting leaves before roots (e.g. deleting)
Inorder - tree has inherent sequence, want to flatten into original sequence

inorder + preorder/postorder uniquely identifies tree
^Subtree of another tree: record both and check