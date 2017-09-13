# https://leetcode.com/problems/range-sum-query-2d-immutable/description/

class NumMatrix(object):
    # will comment out the actual code for better focus but makes it easier to group
    # solution1 = False   # uses cSums; O(mn) space, amortized O(m) time; 219 ms, 9.48%
    # solution2 = True    # cSum of matrixes; O(mn) space, amortized O(1) time; 78 ms, 45.87%
    
    def __init__(self, matrix):
        """
        :type matrix: List[List[int]]
        """
        # solution1:
        # self.cSums = [self.accum(row) for row in matrix]   
        
        # solution2: https://discuss.leetcode.com/topic/29536/clean-c-solution-and-explaination-o-mn-space-with-o-1-time
        # if not matrix or not matrix[0]:  # could just set mSums to null but then would have to check every time in sumRegion
        #     return 0
        numRows = len(matrix)
        numCols = len(matrix[0]) if numRows else 0  # avoid IndexError on [[]]
        self.mSums = [[0]*(numCols+1) for _ in xrange(numRows+1)]  # m[i][j] stores sum of subrect defined by bottom-right (i, j)
        for i in xrange(1, numRows+1):
            for j in xrange(1, numCols+1):
                self.mSums[i][j] = self.mSums[i][j-1] + self.mSums[i-1][j] + matrix[i-1][j-1] - self.mSums[i-1][j-1]
                
        
        
    def accum(self, arr):
        res = [0]*(len(arr)+1)  # store a 0 to simplify if-checks
        for i in xrange(1, len(arr)+1):
            res[i] = res[i-1] + arr[i-1]
        return res  # sum(arr[i] to arr[j]), inclusive = res[j+1] - res[i], since res[k] corresponds to arr[k-1]
        
    def sumRegion(self, row1, col1, row2, col2):  
        """
        :type row1: int
        :type col1: int
        :type row2: int
        :type col2: int
        :rtype: int
        """
        # Solution 1
        # return sum(self.cSums[row][col2+1] - self.cSums[row][col1] for row in xrange(row1, row2+1))
        
        # Solution 2
        return self.mSums[row2+1][col2+1] - self.mSums[row2+1][col1] - self.mSums[row1][col2+1] + self.mSums[row1][col1]
            


# Your NumMatrix object will be instantiated and called as such:
# obj = NumMatrix(matrix)
# param_1 = obj.sumRegion(row1,col1,row2,col2)