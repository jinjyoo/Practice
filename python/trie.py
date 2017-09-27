# https://leetcode.com/problems/implement-trie-prefix-tree/description/
# https://leetcode.com/problems/add-and-search-word-data-structure-design/description/
# https://github.com/yangshun/tech-interview-handbook/blob/master/utilities/python/trie.py

class Node():
    
    def __init__(self):
        # self.char = char  ### actually not needed
        self.is_leaf = False
        self.letters = {}  # will store char: node that has this char (small -> big)

class Trie(object):   # 57%

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.root = Node()  # the root will NOT have a char, but will have children

    def insert(self, word):
        """
        Inserts a word into the trie.
        :type word: str
        :rtype: void
        """
        node = self.root
        for c in word:
            if c not in node.letters:
                node.letters[c] = Node()  
            node = node.letters[c]
        node.is_leaf = True  # points to last node   
        ### Note that this marks an EMPTY node as a leaf, but it is UNIQUE to that letter
        # Cannot mark the node with the last letter itself as a leaf, because it could share that node with other children
        # e.g. "caR", "caSe"      

    def search(self, word):
        """
        Returns if the word is in the trie.
        :type word: str
        :rtype: bool
        """
        node = self.root
        for c in word:
            if c not in node.letters:
                return False
            node = node.letters[c]
        return node.is_leaf  

    def startsWith(self, prefix):
        """
        Returns if there is any word in the trie that starts with the given prefix.
        :type prefix: str
        :rtype: bool
        """
        node = self.root
        for c in prefix:
            if c not in node.letters:
                return False
            node = node.letters[c]
        return True

    def regex(self, word):
        """
        Returns if the word is in the data structure. A word could contain the dot character '.' to represent any one letter.
        :type word: str
        :rtype: bool
        """
        return self.helper(self.root, word, 0)
                        
    def helper(self, node, word, start):  # slicing would create many strings so just carry the start index
        for i in xrange(start, len(word)):
            # if word[i] == '.':
            #     for child in node.letters.itervalues():
            #         if self.helper(child, word, i+1):
            #             return True
            #     return False
            if letter == '.':
                return any(self.helper(child, word, i+1) for child in node.letters.itervalues())
            if word[i] not in node.letters:
                return False
            node = node.letters[word[i]]
        return node.is_leaf
    
    def delete(self, word):  # not asked for, but for practice
        """ 
        Four cases:
        (1) Not in tree - don't do anything
        (2) Is the prefix of a longer word - just mark as not leaf, but don't delete anything
        (3) Only part of it is a word - delete from bottom up to the last (1) leaf node or (2) branching point (exclusive)
        (4) No branches, word is unique - delete every node
        """
        exempt_node = self.root    ### Realization - root should never be deleted, but it can have empty children
        exempt_depth = -1    # index of deletion; root cannot be deleted so index of root is -1
        # delete_start = None      # cannot proactively check if no children, since a later child might have children
        node = self.root
        for depth, c in enumerate(word):
            if c not in node.letters:
            	print "Case 1: Not in trie."
                return   # Case 1, not in tree
            letter = node.letters[c]   ### note that the child is the letter being checked, NOT node
            # Has to be > 1 since == 1 is just the one child that's going to be deleted            
            # cannot exempt last letter if leaf
            if len(letter.letters) > 1 or letter.is_leaf and depth != len(word)-1:   # Setup for Case 3
                exempt_node = letter  # letter is *exempt*, deletions start after 
                exempt_depth = depth
                # exempt_depth += 1    # inaccurate since won't reflect if nodes are skipped 
            node = letter  # Technically unnecessary (could've just assigned to node from start), but clearer this way
        if node.letters:  # Case 2  # at this point, node is the leaf of this word
        	print "Case 2: prefix of a longer word, so don't remove."
        	node.is_leaf = False
        	return
        # Since Case 2 didn't happen, we are deleting something 
        # if exempt_depth == len(word)-1: # this would work but then we'd have lost the actual depth (could've been first letter)
        node = exempt_node   # the place we start deleting from; if None, we don't delete anything (should never be None, though)
     	if node is self.root:
     		print "Case 4: delete every node that makes up this word" 
        if node:  # Case 3; Case 4 if overlap_end = self.root   # technically not needed, otherwise would've been caught in Case 2
            print "Case 3: deleting at least one node (could be all)"
            for c in word[exempt_depth+1:]:
            	node = node.letters.pop(c)  # node was exempt so we check the children

if __name__ == "__main__":
	t = Trie()
	print "Inserting 'pal'";       t.insert("pal"); 
	print "Inserting 'pale'";      t.insert("pale"); 
	print "Deleting 'paler'";      t.delete("paler");   # Case 1   
	print "Inserting 'paler'";     t.insert("paler"); 
	print "Deleting 'pal'" ;       t.delete("pal");     # Case 2
	print "Searching for 'pal'",   t.search("pal");     # False
	print "Searching for 'pale'",  t.search("pale");    # True
	print "Inserting 'pal'";       t.insert("pal");  
	print "Deleting 'paleo'";      t.search("pal");     # True
	print "Inserting 'paleo'";     t.insert("paleo"); 
	print "Inserting 'orange'";    t.insert("orange"); 
	print "Deleting 'orange'";     t.delete("orange")   # Case 4 
	print "Deleting 'paleo'";      t.delete("paleo")    # Case 3 - deleting partially
	print "Searching for 'paleo'", t.search("paleo")    # False
	print "Searching for 'paler'", t.search("paler")    # True

# ["Trie","search", "insert", "search", "startsWith", "search", "insert", "delete"]
# [[],["a"], ["rocks"], ["rock"], ["rock"], ["rocks"], ["rocker"], ["rock"]
# """
# (1) Not in tree - don't do anything
#         (2) Is the prefix of a longer word - just mark as not leaf, but don't delete anything
#         (3) Part of it is a word - delete up to the first leaf node or branching point
#         (4) No branches, word is unique - delete every node

# Case 3a: pal, pale -> delete pale
# Case 3b: 
# """