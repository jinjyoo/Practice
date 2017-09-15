# https://leetcode.com/problems/number-of-islands/description/

# from collections import deque
# followup 1: size of islands
# followup 2: without modifying the grid

class Solution(object):
    def numIslands(self, grid):
        """
        :type grid: List[List[str]]   # Pay attention to the given information...
        :rtype: int
        """
        # return self.solution1(grid)  # 145 ms, 38.97% 
        return self.my_solution(grid)  # 99 ms, 88.00%  # 82 ms, 96.06% with fast version
    
    def solution1(self, grid):  # DFS
        def sink(i, j):
            if 0 <= i < len(grid) and 0 <= j < len(grid[i]) and grid[i][j] == '1':
                grid[i][j] = '0'   # mark as visited                
                # return 1 + sum(map(sink, (i+1, i-1, i, i), (j, j, j+1, j-1)))
                map(sink, (i+1, i-1, i, i), (j, j, j+1, j-1))
                return 1                
            return 0
        # return [sink(i, j) for i in xrange(len(grid)) for j in xrange(len(grid[i])) if sink(i, j) > 0]  # NOT idempotent
        # return filter(lambda x: x > 0, [sink(i, j) for i in xrange(len(grid)) for j in xrange(len(grid[i]))])
        return sum(sink(i, j) for i in xrange(len(grid)) for j in xrange(len(grid[i])))
    
    def solution2(self, grid):  # DFS
        count = 0
        for i in xrange(len(grid)):
            for j in xrange(len(grid[0])):
                if grid[i][j] == '1':
                    self.dfs(grid, i, j)
                    # self.bfs(grid, i, j)
                    count += 1
        return count
    
    def dfs(self, grid, i, j):
        d = [0, 1, 0, -1, 0]
        if (0 <= i < len(grid)) and (0 <= j < len(grid[0])) and grid[i][j] == '1':  # DO need to check, since in recursive, NO checks
            grid[i][j] = '0'   # mark as visited
            for k in xrange(4):
                self.dfs(grid, i+d[k], j+d[k+1])
    
    def my_solution(self, grid):
        res = 0
        for i in xrange(len(grid)):
            for j in xrange(len(grid[0])):
                if grid[i][j] == '1':
                    res += 1
                    self.my_dfs(grid, i, j)
        return res 
        
    def my_dfs(self, grid, i, j):  # assume i, j are valid   # Not BFS...    
        if grid[i][j] == '1': # boundary has not been reached from this direction
            grid[i][j] = '0'
            if j > 0:
                self.my_dfs(grid, i, j-1)
            if j < len(grid[0])-1:
                self.my_dfs(grid, i, j+1)
            if i > 0:
                self.my_dfs(grid, i-1, j)
            if i < len(grid)-1:
                self.my_dfs(grid, i+1, j)
                
    def dfs_fast(self, grid, i, j):  # assume i, j are valid AND grid[i][j] == '1'  # faster, since we have less function calls
        grid[i][j] = '0'
        if j > 0 and grid[i][j-1] == '1':
            self.dfs_fast(grid, i, j-1)
        if j < len(grid[0])-1 and grid[i][j+1] == '1':
            self.dfs_fast(grid, i, j+1)
        if i > 0 and grid[i-1][j] == '1':
            self.dfs_fast(grid, i-1, j)
        if i < len(grid)-1 and grid[i+1][j] == '1':
            self.dfs_fast(grid, i+1, j)  
    
    #Solution 3: BFS
    # Doesn't work for some reason, fix later
    # def bfs(self, grid, i, j):
    #     # queue = deque(((i, j),))
    #     queue = deque([(i, j)])
    #     while queue:
    #         x, y = queue.popleft()
    #         grid[x][y] = '0'
    #         if x > 0 and grid[x-1][y] == '1':  #up
    #             queue.append((x-1, y))
    #             # grid[x-1][y] == '0'
    #         if x < len(grid) and grid[x+1][y] == '1':  #down
    #             queue.append((x+1, y))
    #             # grid[x+1][y] == '0'
    #         if y > 0 and grid[x][y-1] == '1':  #left
    #             queue.append((x, y-1))
    #             # grid[x][y-1] == '0'
    #         if y > 0 and grid[x][y-1] == '1':  #left
    #             queue.append((x, y-1))
    #             # grid[x][y-1] == '0'
                            
                
### Attempt 1 BFS ###
        
#         if not grid[0]: return 0
#         num_islands = 0
#         frontier, visited = deque((0, 0)), set()
#         while frontier:
#             x, y = frontier.pop()
#             # neighbors = self.get_neighbors(grid, x, y)
            
        
#     def get_neighbors(self, grid, x, y):  # just need right and bottom
#         neighbors = []
#         # if x + i < 
#         # return [self.grid[x+i][y+j] for i in (-1, 1) for j in (-1, 1) if x+i  else 0]   
#         # "ask for forgiveness, not permission" 