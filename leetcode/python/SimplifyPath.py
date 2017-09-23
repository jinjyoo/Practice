# https://leetcode.com/problems/simplify-path/description/

class Solution(object):
    def simplifyPath(self, path):
        """
        :type path: str
        :rtype: str
        """
        # return self.solution1(path)  # 43 ms -> 65.14%
        return self.solution2(path)
    
    def solution2(self, path):  # modified from fastest solution
        stack = []
        for i in path.split('/'):
            if not i or i == '.':  # i == ""
                continue           
            if i == "..":
                if stack:
                    stack.pop()
            else:
                stack.append(i)

        return "/" + "/".join(stack)
    
    def solution1(self, path):
        stack = []
        for p in filter(lambda c: c != '.' and c != "", path.split('/')):
            if p == "..":
                if stack:
                    stack.pop()
            else:
                stack.append(p)
        return '/' + '/'.join(stack)
        