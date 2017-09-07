# Kruskal
# Dijkstra

# DFS Cycle
# Topological Sort (BFS + DFS)
# http://www.geeksforgeeks.org/topological-sorting-indegree-based-solution/
# https://www.hackerearth.com/practice/algorithms/graphs/topological-sort/tutorial/

#DFS
# http://www.geeksforgeeks.org/topological-sorting/
# https://en.wikipedia.org/wiki/Topological_sorting#Depth-first_search

# http://www.geeksforgeeks.org/detect-cycle-undirected-graph/
# http://www.geeksforgeeks.org/detect-cycle-in-a-graph/


"""Write cycle detector and print cycle"""
"""Implement both BFS and DFS"""
"""Runtime?  O(n^2)?"""

import unittest
from collections import defaultdict

class Graph(object):   # (object) makes this a new-style class
    def __init__(self, vertices):  
        self.graph = defaultdict(list)  # adj_list
        self.size = len(vertices)

    def add_edge(self, u, v):
        self.graph[u].append(v)

    # def __str__(self):
    #     raise NotImplementedError("Should have implemented this")

class GraphD(Graph):
    def __init__(self, vertices):
        super(GraphD, self).__init__(vertices)

    def dfs_cycle(self):  ### "dft" is more accurate since we're doing a traversal, not a search
        pass

    def print_cycle(self):
        pass

class Dag(GraphD):
    def __init__(self, vertices):
        super(Dag, self).__init__(vertices)

    def dfs_topo(self):
        pass

    def bfs_topo(self):
        pass

class GraphU(Graph):   # Undirected graph   
    def __init__(self, vertices):
        super(GraphU, self).__init__(vertices)
        # super()__init__(vertices)  # Python 3

    def add_edge(self, u, v):
        # super(GraphU, self).add_edge(u, v)  # slower
        self.graph[u].append(v)
        self.graph[v].append(u)

    def dfs_cycle1(self):  # iterative
        visited = {vertex:False for vertex in self.graph.iterkeys()} 
        stack = [next(self.graph.iterkeys())]  # get first element
        while stack:   
            node = stack.pop()
            visited[node] = True
            # stack.extend(self.graph[node])
            for neighbor in self.graph[node]:
                if visited[neighbor]:
                    return True
                stack.append(neighbor)
        return False

    def dfs_cycle2(self):  # recursive
        visited = set()    # better than dict
        stack = [next(self.graph.iterkeys())]  # get first element
        return self.dfs(stack, visited)

    def dfs(stack, visited):
        if not stack:
            return False  # no cycle
        node = stack.pop()
        if node in visited:
            return True
        visited.add(node)
        return self.dfs(stack, visited)
        

    def bfs_cycle(self):
        pass

    def kruskal(self):
        pass

    def dijkstra(self):
        pass

    
    # def test(self):   # all methods must begin with 'test'
g = GraphU(['A', 'B', 'C', 'D'])        
g.add_edge('A', 'B')
g.add_edge('B', 'D')
g.add_edge('D', 'C')
g.add_edge('C', 'B')
print g.dfs_cycle()
# self.assertEqual(g.dfs_cycle(), True)
# self.assertTrue(g.dfs_cycle(), msg="There is a cycle.")
        # g.add_edge()

# if __name__ == '__main__':
#     unittest.main()

