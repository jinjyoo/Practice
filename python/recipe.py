import itertools as it

"""Primes"""  
# https://stackoverflow.com/questions/2068372/fastest-way-to-list-all-primes-below-n
# https://stackoverflow.com/questions/622/most-efficient-code-for-the-first-10000-prime-numbers?noredirect=1&lq=1
# ^See: Sieve of Atkins
def sieve(k=20232):  
    is_prime = [True]*k 
    for i in xrange(2, k):  # GO up to k and not sqrt(k) since we use is_prime to yield
        if is_prime[i]:
            yield i      
        for j in xrange(i*i, k, i):  # important optimization -> start at i*i, since i*2, etc. are already set
            is_prime[j] = False

def primes(n):
    """ Returns  a list of primes < n """   ### LESS THAN
    prime = [True] * n
    for i in xrange(3,int(n**0.5)+1,2):  # does not set even numbers to False
        if prime[i]:
            prime[i*i::2*i] = [False]*((n - i*i - 1) / (2*i) + 1)
    return [2] + [i for i in xrange(3, n, 2) if prime[i]]

# https://stackoverflow.com/questions/2211990/how-to-implement-an-efficient-infinite-generator-of-prime-numbers-in-python
# http://www.macdevcenter.com/pub/a/python/excerpt/pythonckbk_chap1/index1.html?page=2  
def erat():
    sieve = {}
    yield 2
    for q in it.islice(it.count(3), 0, None, 2):
        p = sieve.pop(q, None)
        if p is None:
            sieve[q*q] = q
            yield q
        else:
            # x = p + q   # Old code
            # while x in D or not (x&1):
            #     x += p
            x = q + 2*p    
            while x in D:
                x += 2*p
            sieve[x] = p

"""Decorators"""
def memo(func):
    def wrapper(x):
        cache = {}
        if x not in cache:
            cache[x] = func(x)
        return cache[x]
    return wrapper


from timeit import default_timer as timer
def timer(func):
    def wrapper(*args, **kwargs):
        t1 = timer()   # matches to time.clock() or time.time(), based on OS
        res = func(*arg, **kw)
        t2 = timer()
        return (t2 - t1), res, func.__name__
    return wrapper


def gcd(u, v):
    return gcd(v, u % v) if v else abs(u)

def unbounded_backpack(V, W, weight):  # unbounded
    dp = [0 for _ in xrange(weight+1)]  # dp[i] is max weight <= i
    dp[0] = 0
    for i in xrange(1, len(dp)):
        dp[i] = max([V[i] + dp[i-W[i]] for i in xrange(len(W)) if item <= i])
    return dp[weight]

def bounded_backpack(V, W, weight):  # bounded, 0-1
    dp = [[0]*(weight+1) for _ in xrange(len(V)+1)]  # dp[i][w] is the max weight <= w you can get with the first i items
    for i in xrange(1, len(V)+1):  # each item
        for j in xrange(weight):  # each weight  # can't take shortcut and start at items[i], need to get every entry
            if W[i] > j: 
                dp[i][w] = dp[i-1][w]
            else:
                dp[i][j] = max(dp[i-1][j], V[i] + dp[i][j-W[i]])
    return dp[len(V)][weight]

def rolling_array(V, W, weight):  # TODO
    pass

# Can also use Fibonacci heap to keep track of lowest distance
# O(E + V log V) time, O(V) space.  With binary heap: O((E+V) log V) time.
def dijkstra(graph, start, target=None):  # G = {0:{1:4, 3:2, ...}, 1:{}} - adjacency list
    res = {start:0}  # res is not necessary if there's a target
    dist = {vertex:float("inf") for vertex in graph if vertex != start}  # stores tentative distance from start
    ### ^Should use a heap to efficiently get min_distance
    # dist = heapq.heapify(dist)
    while dist:  
        node = min(dist, key=dist.get)  # get key corresponding to smallest value; random if multiple
        for neigh in graph[node]:
            new_dist = dist[neigh] + graph[node][neigh]
            if new_dist < dist[node]:
                dist[node] = dist
        res[node] = dist.pop(node)  
        if target and node == target:
            return res[target]
    return res

def dijkstra2(graph, start, target=None):  # TODO
    visited = {start}
    not_visited = {graph.keys()} - {start}  # static view
    while not_visited:
        pass

def stringToTreeNode(input):
    input = input[1:-1]
    if not input:
        return None
    inputValues = [s.strip() for s in input.split(',')]
    root = TreeNode(int(inputValues[0]))
    nodeQueue = [root]
    front = 0
    index = 1
    while index < len(inputValues):
        node = nodeQueue[front]
        front = front + 1
        item = inputValues[index]
        index = index + 1
        if item != "null":
            leftNumber = int(item)
            node.left = TreeNode(leftNumber)
            nodeQueue.append(node.left)
        if index >= len(inputValues):
            break
        item = inputValues[index]
        index = index + 1
        if item != "null":
            rightNumber = int(item)
            node.right = TreeNode(rightNumber)
            nodeQueue.append(node.right)
    return root

def treeNodeToString(root):
    output = ""
    queue = [root]
    length = 1
    current = 0
    while current != length:
        node = queue[current]
        current = current + 1

        if not node:
            output += "null, "
            continue

        output += str(node.val) + ", "
        queue.append(output.left)
        queue.append(output.right)
    return "[" + output[:-2] + "]"

import sys
def readlines():
    for line in sys.stdin:
        yield line.strip('\n')

def main():
    lines = readlines()
    while True:
        try:
            line = lines.next()
            root = stringToTreeNode(line)
            line = lines.next()
            m = int(line)
            line = lines.next()
            n = int(line)
            
            ret = Solution().lowestCommonAncestor(root, m, n)

            out = treeNodeToString(ret)
            print out
        except StopIteration:
            break

if __name__ == '__main__':
    main()