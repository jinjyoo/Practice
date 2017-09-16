# https://leetcode.com/problems/surrounded-regions/description/

"""
["XXXX","XOOX","XXOX","XOXX"]
["XXXX", "XOXX", "XOOX", "XXOX"]
[]
["O"]
["OO", "OO"]
["XXXX", "XOOX", "XOOX", "XXXX"]
["XXXXXXXXXXXXXXXXXXXX","XXXXXXXXXOOOXXXXXXXX","XXXXXOOOXOXOXXXXXXXX","XXXXXOXOXOXOOOXXXXXX","XXXXXOXOOOXXXXXXXXXX","XXXXXOXXXXXXXXXXXXXX"]
["XOXOXO","OXOXOX","XOXOXO","OXOXOX"]
"""

class Solution(object):
    def solve(self, board):
        """
        :type board: List[List[str]]
        :rtype: void Do not return anything, modify board in-place instead.
        
        Note: Used DFS but worst case space requirement is O(mn) of recursive stack calls, so BFS might be better.
        """
        # self.solution1(board)  # 269 ms, 16.52%
        return self.solution2(board)  # 129 ms, 84.67%
           
    def solution1(self, board):  # O(mn) time  # O(mn) space worst case
        """Look at the border and starting from each 'O', do a traversal to find connected components and mark as not marked.
        Then do a traversal and mark every 'O' that wasn't marked.  Worst case, two traversals of whole graph (whole graph of 'O's)
        
        Improvement: could reduce to O(1) space by marking visited as something like '1' instead, then changing during final traversal.
        """
        if len(board) > 2 and len(board[0]) > 2:  # causes extra indentation but would require extra check if switched 
            self.visited = set()  # will record pieces that can't be captured, because they're reachable from a border 'O'
            m, n = len(board), len(board[0]) 
            for j in xrange(n):
                if board[0][j] == 'O' and (0, j) not in self.visited:  
                    self.dfs(board, 0, j)
                if board[m-1][j] == 'O' and (m-1, j) not in self.visited:  # use n-1 instead of -1 because of dfs bound checks
                    self.dfs(board, m-1, j)
            for i in xrange(1, m-1):  # don't need to do top and bottom rows
                if board[i][0] == 'O' and (i, 0) not in self.visited:
                    self.dfs(board, i, 0)
                if board[i][n-1] == 'O' and (i, n-1) not in self.visited:
                    self.dfs(board, i, n-1)
            for i in xrange(1, m-1):
                for j in xrange(1, n-1):
                    if board[i][j] == 'O' and (i, j) not in self.visited:
                        board[i][j] = 'X'
                             
    def dfs(self, board, i, j):  # (i, j) are valid
        self.visited.add((i, j))
        if i > 1 and board[i-1][j] == 'O' and (i-1, j) not in self.visited:
            self.dfs(board, i-1, j)
        if i+1 < len(board) and board[i+1][j] == 'O' and (i+1, j) not in self.visited:
            self.dfs(board, i+1, j)
        if j > 1 and board[i][j-1] == 'O' and (i, j-1) not in self.visited:
            self.dfs(board, i, j-1)
        if j+1 < len(board[0]) and board[i][j+1] == 'O' and (i, j+1) not in self.visited:
            self.dfs(board, i, j+1)
        
    # Modified from: https://discuss.leetcode.com/topic/18706/9-lines-python-148-ms  # Fastest submitted solution
    def solution2(self, board):  # save uses O(m+n) space
        if not any(board): return
        m, n = len(board), len(board[0])
        # save = [ij for k in xrange(max(m, n)) for ij in ((0, k), (m-1, k), (k, 0), (k, n-1))]  # Unnecessary additions here...
        save = [ij for k in xrange(n) for ij in ((0, k), (m-1, k))] + [ij for k in xrange(1, m-1) for ij in ((k, 0), (k, n-1))]
        while save:
            i, j = save.pop()
            if 0 <= i < m and 0 <= j < n and board[i][j] == 'O':
                board[i][j] = 'S'
                save += (i, j-1), (i, j+1), (i-1, j), (i+1, j)
        board[:] = [['XO'[c == 'S'] for c in row] for row in board]
        

    def solution3(self, board):  # BFS solution: https://discuss.leetcode.com/topic/23903/python-short-bfs-solution
        queue = collections.deque()
        for r in xrange(len(board)):  # could speed up the border initialization
            for c in xrange(len(board[0])):
                if (r in (0, len(board)-1) or c in (0, len(board[0])-1) and board[r][c] == "O":
                    queue.append((r, c))
        while queue:
            r, c = queue.popleft()
            if 0<=r<len(board) and 0<=c<len(board[0]) and board[r][c] == "O":
                board[r][c] = "D"
                queue.append((r-1, c)); queue.append((r+1, c))
                queue.append((r, c-1)); queue.append((r, c+1))
        for r in xrange(len(board)):
            for c in xrange(len(board[0])):
                if board[r][c] == "O":
                    board[r][c] = "X"
                elif board[r][c] == "D":
                    board[r][c] = "O"
                    
    def solution4(self, board):   # https://discuss.leetcode.com/topic/1944/solve-it-using-union-find
        pass  # Interesting Union-Find version, but would need to translate to Python first
        
#     def attempt1(self, board):  # O(mn)
#         """
#         We don't have to check outer border, since nothing there can be surrounded
#         """
#         self.visited = set()  # will keep track of O's
#         if len(board) > 2 and len(board[0]) > 2:
#             for i in xrange(1, len(board)-1):
#                 for j in xrange(1, len(board[0])-1):
#                     if board[i][j] == 'O' and (i, j) not in self.visited:  # visited check necessary for correctness, and faster
#                         self.dfs_attempt(board, i, j)
                    
    
#     # DFS will probably be faster than BFS
#     def dfs_attempt(self, board, i, j):  # board[i][j] is unvisited 'O'
#         """
#         Fails for cases where one side is closed but the other is not.  To fix, would have to just record starts, check if 
#         nothing failed, and then revisit the connected component and mark if false (second traversal for the 'O's).  
#         But that's getting really slow...  Also could move 'X' marking and then avoid all this redundant code.  
#         """
#         print (i, j)
#         self.visited.add((i, j))
#         board[i][j] = 'X'
#         if j == 0:  # we reached the end, and still no 'X' boundary
#             print 'fail 0'
#             board[i][j] = 'O'
#             return False
#         elif board[i][j-1] == 'O' and (i, j-1) not in self.visited:  # still need to search for left bound
#             if not self.dfs(board, i, j-1):
#                 print 'fail 1'
#                 board[i][j] = 'O'
#                 return False
#         if j == len(board[0])-1:  
#             print 'fail 2'
#             board[i][j] = 'O'
#             return False
#         elif board[i][j+1] == 'O' and (i, j+1) not in self.visited:  # right bound
#             if not self.dfs(board, i, j+1):
#                 print 'fail 3:', i, j+1
#                 board[i][j] = 'O'
#                 return False
#         if i == 0:
#             print 'fail 4'
#             board[i][j] = 'O'
#             return False
#         elif board[i-1][j] == 'O' and (i-1, j) not in self.visited:  # top bound
#             if not self.dfs(board, i-1, j):
#                 print 'fail 5'
#                 board[i][j] = 'O'
#                 return False
#         if i == len(board)-1:  # we reached the end, and still no 'X' boundary
#             print 'fail 6'
#             board[i][j] = 'O'
#             return False
#         elif board[i+1][j] == 'O' and (i+1, j) not in self.visited:  # bottom bound
#             if not self.dfs(board, i+1, j):
#                 print 'fail 7:', i+1, j
#                 board[i][j] = 'O'
#                 return False
#         print 'Final result: ', board[i][j], i, j
#         return True  # so far so good
           
            