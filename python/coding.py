"""
def quick_sort(lst):
	if len(lst) <= 1:  #0-1
		return lst
	else:
		pivot = lst[0]
		# less = filter(lambda x, pivot: x < pivot, lst, pivot)
		less = []
		greater = []
		equal = []
		for x in lst:
			if x < pivot:
				less.append(x)
			elif x > pivot:
				greater.append(x)
			else:
				equal.append(x)
		return quick_sort(less) + equal + quick_sort(greater)

def merge_sort(lst):
    if len(lst) <= 1:
        return lst
    mid = len(lst) // 2
    left = merge_sort(lst[:mid])
    right = merge_sort(lst[mid:])
    return merge(left, right)

def merge(left, right):
    if not left: #left is null
        return right
    if not right:
        return left
    if left[0] < right[0]:
        return [left[0]] + merge(left[1:], right)
    else:
        return [right[0]] + merge(left, right[1:])


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

#OOP 
print max(mylist, key=len)

if __name__ == "__main__":
    x = LinkedList() #no "new"
    y = LinkedList()
    x.head.next = Node(5)
    x.__dict__
    LinkedList.creator = "Yoojong"
    LinkedList.__dict__
    #getattr(x, 'energy', 100) #default if 'energy' is not defined
    #obj == eval(repr(obj))
    #private methods: _Robot__age

while True:
    try:
        n = raw_input("Please enter an integer: ")
        n = int(n)
        break
    except ValueError:  # IOError, etc.
        print("No valid integer! Please try again ...")
    except (IOError, OverflowError, AttributeError):
	    print "An I/O error or a ValueError occurred"
	except:
	    print "An unexpected error occurred"
	    raise
	else:
		print 'No errors!'
	finally:
		print 'Yohoho and a bottle of rum'
print "Great, you successfully entered an integer!"

        # self.__priv = "I am private"  # N/A, just mangles name to prevent namespace collisions with subclasses
        # self._prot = "I am protected" # can be read and written; just a warning ("others shouldn't see this")
        # self.pub = "I am public"      # can be read and written
"""


    @classmethod  # can use the class and its properties instead of particular instance
    # # most common use - define alternative constructors
    def get_num_trees(cls):  # because "cls", will be overridden if used by inherited class
        return cls.get_num_trees

    # abstract method
    def get_radius(self):  # problem: only triggers when called.  See below:
        raise NotImplementedError

    # import abc
    # @abc.abstractmethod
    # def get_radius(self):
    #     """Method that should do something"""

    @staticmethod   # just a normal function that happens to be defined in a class
    # also means you don't reference Class explicitly, so subclasses can use it just fine
    def celebrate():
        print("Hi, I don't need no class or instance.")


def sum_of_two_numbers(arr, target, low=0, high=len(arr)-1):
    low, high = 0, len(arr) - 1
    while low < high:  # solves empty case
        s = arr[low] + arr[high]
        if s == target:
            return True
        elif s > target:
            return sum_of_
    return sum_of_two_numbers()

# Enter your code here. Read input from STDIN. Print output to STDOUT
n, m = map(int, raw_input().strip().split(' '))
p = map(int, raw_input().strip().split(' '))
q = map(int, raw_input().strip().split(' '))


class Solution(object):
    def isSubtree(self, s, t):
        """
        :type s: TreeNode
        :type t: TreeNode
        :rtype: bool
        """
        def tree2Str(root):
            array = []
            def inorder(root):
                if root:
                    array.append('(')
                    inorder(root.left)
                    array.append(str(root.val))
                    inorder(root.right)
                    array.append(')')
                else:
                    array.append('#')
            inorder(root)
            return ''.join(array)
        main_str = tree2Str(s)
        sub_str = tree2Str(t)
        return (sub_str in main_str) and sub_str != ''

        def convert(p):
            return "^" + str(p.val) + "#" + convert(p.left) + convert(p.right) if p else "$"
        return convert(t) in convert(s)


def preorderTraversal(self, root):
        if not root: return []
        ret = []
        stack = [root]   # DFS uses stack
        while stack:
            node = stack.pop()
            ret.append(node.val)  # preorder, root comes first
            if node.right:
                stack.append(node.right)  
            if node.left:
                stack.append(node.left)  # left is done last, so it'll be processed first
        return ret

def inorderTraversal(self, root):
    if not root: return []
    ret = []
    stack = [root]
    while stack:
        node = stack.pop()
        if node.right:

def postorderTraversal(self, root):
    if not root: return []
    ret = []
    stack = [root]
    while stack:


class Solution(object):
    def isBalanced(self, root):
        def check(root):
            if root is None:
                return 0
            left  = check(root.left)
            right = check(root.right)
            if left == -1 or right == -1 or abs(left - right) > 1:
                return -1
            return 1 + max(left, right)
        return check(root) != -1


def deleteNode(self, root, key):
    """
    :type root: TreeNode
    :type key: int
    :rtype: TreeNode
    """
    if not root:
        return
    if root.val == key:
        if not root.right:
            return root.left
        else:
            node = root.right
            while node.left:
                node = node.left
            node.left = root.left 
            return root.right
    elif root.val > key:
        root.left = self.deleteNode(root.left, key)
    else:
        root.right = self.deleteNode(root.right, key)
    return root

def isSymmetric(self, root):
    return symmetry(self.root)

def symmetry(self, left, right):
    if not (left or right): return True
    if not (left.val == right.val): return False
    return self.symmetry(left.left, right.right) and self.symmetry(left.right, right.left)

    return symmetry(node.left, node.right)

    node.left.right == node.right.left
    node.left.left == node.right.right
    
def divide(a, b):
    result = None
    try:
        result = a / b
    except ZeroDivisionError:
        print("Type error: division by 0.")
    except TypeError:   # E.g., if b is a string       
        print("Type error: division by '{0}'.".format(b))  
    except Exception as e:   # handle any other exception       
        print("Error '{0}' occured. Arguments {1}.".format(e.message, e.args))
    else:  # Executes if no exception occured   
        print("No errors")
    finally:   # Executes always      
        if result is None:
            result = 0
    return result

class Rectangle(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.area = width * height

class Square(Rectangle):
    def __init__(self, length): # one argument
        super(Square, self).__init__(length, length)    # Python2
        super().__init__(length, length) # Python3
s = Square(5)
print(s.area)  # 25


from collections import namedtuple
def get_name():
    name = namedtuple("name", ["first", "middle", "last"])
    return name("Richard", "Xavier", "Jones")
name = get_name()
# much easier to read
print(name.first, name.middle, name.last)

#Direction arrays:
for k in xrange(4):
    sink(grid, i+d[k], j+d[k+1])
d = [0, 1, 0, -1, 0]

[entry if tag in entry else [] for tag in tags for entry in entries]

row = [kid for node in row for kid in (node.left, node.right) if kid]
# Longhand - outer loops, then inner
for node in row:
    for kid in (node.left, node.right):
        if kid:
            xxx += kid,

level = [kid for node in level for kid in (node.left, node.right) if kid]  


# Positional arguments
def foo(*positional, **keywords):
    print "Positional:", positional
    print "Keywords:", keywords
foo('one','two',c='three',d='four')

"""Generators"""
def f123():
    yield 1
    yield 2  # if called again, this is where it resumes
    yield 3  # cf: 3 return statements

def f():
    for i in xrange(5):
        yield i
# f() = <generator object>
# next(f()) will repeatedly return 0, because "f()" recreates generator
# g = f()
# next(g) will return properly

def get_primes(number):
    while True:  # this is VERY important, otherwise with repeated next(), number += 1 and then generator is finished
        if is_prime(number):
            yield number
        number += 1

p = protocol()
p.next() # advance to the yield statement, otherwise I can't call send  #Gotcha
p.send(5)  #TypeError: can't send non-None value to a just-started generator

def infinity(start):
    yield start
    yield from infinity(start + 1)
    # for x in infinity(start + 1):
    #     yield x 

def grep(pattern):
    print "Looking for %s" % pattern
    while True:
        line = (yield)
        if pattern in line:
            print line,
# Example use
if __name__ == '__main__':
    g = grep("python")
    g.next()
    g.send("Yeah, but no, but yeah, but no")
    g.send("A series of tubes")
    g.send("python generators rock!")

"Printing"
print '{0:.2}'.format(1.0 / 3)  # 0.33
print '{0:-2%}'.format(1.0 / 3) # 33.33%


"Gotcha" #https://leetcode.com/problems/kth-smallest-element-in-a-bst/#/description
self.index = k
return self.inorder2(root)  # guaranteed to be valid
    
def inorder2(self, node):
    if node:
        print node.val, self.index
        self.inorder2(node.left)
        if self.index == 1:
            print node.val, 'hi'
            return node.val  # guaranteed to terminate
        self.index -= 1
        self.inorder2(node.right)

Check this:
carryover = 0
for i in xrange(len(digits)-1, 0, -1): 
    carryover = 1
print carryover

digits[-1], carryover = digits[-1]%10, digits[-1]/10
while carryover:  # same id?
    carryover = 1

import sys
"""======================================"""
# Enter your code here. Read input from STDIN. Print output to STDOUT
import sys 

N, Q = map(int, raw_input().strip().split(' '))
lastAns = 0
seqList = [[] for i in xrange(N)]
for i in xrange(Q):
    #user_input = raw_input().strip().split(' ')
    #print "On query " + str(i)
    query_type, x, y = map(int, raw_input().strip().split(' '))
    #print query_type, x, y
    index = (x^lastAns)%N;                       
    if query_type == 1:
        seqList[index].append(y)
    if query_type == 2:
        seq = seqList[index]                   
        lastAns = seq[y % len(seq)]
        print lastAns                           
 

N, Q = map(int, raw_input().strip().split(' '))
n, inputs = [int(n) for n in input().split(" ")]
