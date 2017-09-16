"""
visited = set(), but can be [False]*len(graph) if nodes are numbers
"""


"""http://eddmann.com/posts/depth-first-search-and-breadth-first-search-in-python/"""
"""Get connected components from _start_: DFS (recur+iter), BFS (iter)"""
def dfs_bad(graph, start, visited=None):  # Recursive
    if visited is None:     # Costly if-check, probably better to just have a wrapper function that passes one in
        visited = set()
    visited.add(start)
    """Incorrect. It will subtract the visited set according to how visited was set when the call was first made. So when 
    the recursive calls are made and change visited, the original call ignore those changes and visits nodes that were 
    already visited. """
    for next in graph[start] - visited:   # Only static view, so incorrect
        dfs_bad(graph, next, visited)
    return visited          # Does not preserve order?

# no wrapper function used, but it costs extra for the base case
def dfs_recursive_connected(graph, node, visited=None):   # correct version
	if visited is None:   
		visited = set()
	print 'Visiting', node
	visited.add(node)
	for next in graph[node]:  # static view for graph[node] but that's okay since graph will not change
		if next not in visited:  
			dfs_recursive_connected(graph, next, visited)
	return visited

def dfs_iter_connected(graph, start):  
	# Alternatively: start = [next(graph.iterkeys())]
    visited, stack = set(), [start]
    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            visited.add(vertex)
            stack.extend(graph[vertex] - visited)
    return visited   # reachable

from collections import deque
def bfs_connected(graph, start):    # almost exactly the same as dfs_iter_connected
    visited, queue = set(), deque([start])
    while queue:
        vertex = queue.popleft()
        if vertex not in visited:
            visited.add(vertex)
            queue.extend(graph[vertex] - visited)
    return visited

"""Print all paths to goal"""
def dfs_paths_recursive(graph, start, goal, path=None):   # Recursive   # Python3
    if path is None:
        path = [start]
    if start == goal:
        yield path
    for next in graph[start] - set(path):
        yield from dfs_recursive_paths(graph, next, goal, path + [next])
# list(dfs_paths(graph, 'A', 'F'))   # don't forget to materialize generator

def dfs_paths_iter(graph, start, goal):  # Print all possible paths to goal   # Iterative
    stack = [(start, [start])]
    while stack:
        (vertex, path) = stack.pop()
        for next in graph[vertex] - set(path):
            if next == goal:
                yield path + [next]
            else:
                stack.append((next, path + [next]))

def bfs_paths(graph, start, goal):
    # queue = [(start, [start])]
    queue = deque([(start, [start])])
    while queue:
        (vertex, path) = queue.popleft()
        for next in graph[vertex] - set(path):
            if next == goal:
                yield path + [next]
            else:
                queue.append((next, path + [next]))

"""Only with BFS"""
def shortest_path(graph, start, goal):  # the shortest path will be returned first from the BFS path generator method (cf: DFS)
    try:								
        return next(bfs_paths(graph, start, goal))
    except StopIteration:
        return None

"""Cycle detection on an undirected graph"""
# return if there are cycles in the connected component from start _only_
"""BFS version is almost exactly the same as this, so not shown"""
def dfs_undirected_cycle_iter(graph, start):   # iter
	visited = set()			### comment out for dfs_all below
	stack = [(start, -1)]   # node, parent
	while stack:
		node, parent = stack.pop()
		for neighbor in graph[node]:
			if neighbor in visited and neighbor != parent:
				return True  # cycle
			# stack.extend(graph[node] - visited)
			else:
				stack.append(neighbor)
	return False

def dfs_all_undirected_cycle_iter(graph, start):  # get all connected components
	visited = set()
	# has_cycle = False  # global variable
	for node in graph:
		if node not in visited:  # _visited_ will be updated as dfs_util is called
			if dfs_undirected_cycle_iter(graph, node):   # we DON'T return True since this is just an efficiency measure
				return True
	return False

def dfs_undirected_cycle_recursive(graph):  # recursive
	# visited = [False]*len(graph)   ### Only if nodes are numbers
	visited = set()
	for node in graph:   # necessary to get all connected components
		if node not in visited:
			# return any(dfs_util(graph, visited, graph[node]) for node in graph if node not in visited)  
			### ^doesn't work since visited isn't updated(?)
			if dfs_util(graph, visited, graph[node], -1):  # -1 is dummy value for parent
				return True
	return False

def dfs_util(graph, visited, node, parent):  # util for above
	visited.add(node)
	for neighbor in graph[node]:
		if neighbor not in visited:   # don't need to check neighbor != parent since it should be in visited
			dfs_util(graph, visited, neighbor, node)
		# if neighbor in visited  and neighbor != parent:   
		elif neighbor != parent:      
			return True
	return False  # no cycles in the neighbors reachable from this node

"""Cycle detection on a recursive graph: DFS only, but can use BFS via topological sort"""
def dfs_directed_cycle_recursive(graph): # http://www.geeksforgeeks.org/detect-cycle-in-a-graph/
	# visited = [False] * len(graph)
	visited, rec_stack = set(), set()
	# return all(cyclic_util(node, visited, recStack) for node in graph)  # don't do, unless switch False w/ True
    for node in xrange(len(graph)):   # get all connected components      # ^Also, inefficient w/ redundant calls [visited]
        if node not in visited:       
            if cyclic_util(node, visited, recStack):
                return True
    return False

def cyclic_util(start, visited, rec_stack):
	visited.add(start)
	rec_stack.add(start)
    for node in graph[start]:
        if node not in visited:  # unlike directed, don't need to check if not parent 
            if cyclic_util(node, visited, rec_stack):
                return True
        elif node in rec_stack:  # implies that node is also in visited, so no need to check that   # check for back edges
            return True          # could be visited but NOT on rec_stack; e.g. (A->B->C, A->C)
    rec_stack.delete(start)  # We found no cycles in the subgraph reachable from _start_, but some other node might be
    return False			 # able to reach this node ([at least] one one-way path to _start_, so no cycle
    						 # Keep in _visited, since that just lessens calls to cyclic_util

# Basically same as above, but only uses one dict instead of two lists
def dfs_directed_cycle_colors(graph):  # http://www.geeksforgeeks.org/detect-cycle-direct-graph-using-colors/  #CLRS
	# color = ['white'] * len(graph)
	colors = {node:'white' for node in graph.iterkeys()}
    for node in colors:
        if colors[node] == 'white':
            if color_cycle(node, colors):
                return True
    return False	

# White - not visited; Gray: on rec_stack (function call stack), being processed; Black: vertex and all descendants processed
"""https://cs.stackexchange.com/questions/9676/the-purpose-of-grey-node-in-graph-depth-first-search"""
# If _node_ is seen after all of its descendants had been seen, that means that the current node _curr_ was not among 
# _node_’s descendants, so the current link is one-way and thus not a cycle
def color_cycle(graph, colors, start):
    colors[start] = 'gray'
    for node in graph[start]:
        if colors[node] == 'white':
            if color_cycle(graph, colors, node):  
                return True
        elif colors[node] == 'gray':  # if node in rec_stack; gray -> back edge
            return True
        # else:  # black -> skip
    colors[start] = 'black'  # not white (so it's been visited), but not on rec_stack
    return False

"""Topological sort - can also be used to check for cycles"""
""" https://www.hackerearth.com/practice/algorithms/graphs/topological-sort/tutorial/ """
""" https://en.wikipedia.org/wiki/Topological_sorting#Depth-first_search """ 
# Note that a vertex is pushed to stack only when all of its adjacent vertices 
# (and their adjacent vertices and so on) are already in stack.
# http://www.geeksforgeeks.org/topological-sorting/ 
"""Basically the same as color_cycle or rec_stack"""
def dfs_topological_check(graph):  
    colors = {node:'white' for node in graph.iterkeys()}
    topo_sort = deque()
    for node in colors:
        if colors[node] == 'white':
            if not color_cycle(node, colors, topo_sort):  # returned None
                return None  # not a dag
    return topo_sort

def topo_util(graph, start, topo_sort):   
    colors[start] = 'gray'   # temporary mark
    for node in graph[start]:
        if colors[node] == 'white': 
            if not color_cycle(graph, colors, node): 
            	return None
        elif colors[node] == 'gray':  
            return None   # not a dag
        # else:  # black -> skip
    colors[start] = 'black'  # permanent mark
    topo_sort.appendleft(start)   # See Wiki link above
    # https://discuss.leetcode.com/topic/13873/two-ac-solution-in-java-using-bfs-and-dfs-with-explanation/2
    # ^The ones turned black last are the ones with the most children, so they should be put first
    # The ones turned black first have few recursive calls afterward (few children), so should wind up last
    # Alternatively, append() and then reverse at end
    return True  # so far, is a dag

from itertools import chain
# https://www.hackerearth.com/practice/algorithms/graphs/topological-sort/tutorial/
# http://www.geeksforgeeks.org/topological-sorting-indegree-based-solution/
def bfs_topological_check(graph):    # Kahn's algorithm
	indegrees = {node:0 for node in graph}  
	topo_sort = []
	# for node in graph.itervalues():  # cannot do this because itervalues() will return lists
	for node in chain.from_iterable(graph.itervalues()):
		indegrees[node] += 1  
	# for neighbors in graph.itervalues():   # alternative to above
	# 	for node in neighbors:
	# 		indegrees[node] += 1
	queue = deque([node for node, indegree in indegrees.iteritems() if indegree == 0])
	"""^Note: this works for multiple connected components, since each root should've been added here"""
	# queue = deque()   # alternative to above
	# for node, indegree in indegrees.iteritems():
	# 	if indegree == 0:
	# 		deque.append(node)	
	while queue:
		node = queue.popleft()   # if len(queue) > 1, there are multiple possible sorts
		topo_sort.append(node)
		for node in graph:
			for neighbor in graph[node]: 
				indegree[neighbor] -= 1  
				if indegree[neighbor] == 0:
					queue.append(node)
					# topo_sort.append(node)
	if len(topo_sort) != len(graph):  # if different, then there IS a cycle  
		return None  # Not a dag
	return topo_sort



["XXXXXXXXXXXXXXXXXXXX",
"XXXXXXXXXOOOXXXXXXXX",
"XXXXXOOOXOXOXXXXXXXX",
"XXXXXOXOXOXOOOXXXXXX",
"XXXXXOXOOOXXXXXXXXXX",
"XXXXXOXXXXXXXXXXXXXX"]


["XXXXXXXXXXXXXXXXXXXX","XXXXXXXXXOOOXXXXXXXX","XXXXXOOOXOXOXXXXXXXX","XXXXXOXOXOXOOOXXXXXX","XXXXXOXOOOXXXXXXXXXX","XXXXXOXXXXXXXXXXXXXX"]
