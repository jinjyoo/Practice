# Peterson   # https://cs.stackexchange.com/questions/12621/contrasting-peterson-s-and-dekker-s-algorithms
# https://stackoverflow.com/questions/4849077/unable-to-understand-correctness-of-peterson-algorithm
flag[0] = True
turn = 1  # first yield to the other process
# Turn is needed; e.g. both p0 and p1 want to go, but then they keep busy waiting for each other (deadlock)

while flag[1] == True and turn == 1:  # check flag first because turn was just set
	pass
critical_section()
flag[0] = False

# Dekker
flag[0] = True
while flag[1] == True:
	if turn != 0:
		flag[0] = False
		while turn != 0:   # Could combine with if statement, but faster with pass instead of repeated assignment
			pass
		flag[0] = True
critical_section()
turn = 1
flag[0] = False


def gcd(u, v):
    return gcd(v, u % v) if v else abs(u)

# https://prismoskills.appspot.com/lessons/Programming_Puzzles/Lexicographical_minimum_in_string.jsp
# O(n) because even when i 'resets', it will not revisit any letter more than twice
def booth(s):
	"""
	>>> booth('alabala')
	'abalaal'
	>>> booth('bbaaccaadd')
	'aaccaaddbb'
	>>> booth('baabaa')
	'aabaab'
	>>> booth('ABABCABA')
	'AABABCAB'
	>>> booth('ababa')
	'aabab'
	>>> booth('aabaabaaab')
	'aaabaabaab'
	>>> booth('bbbbbbbba')
	'abbbbbbbb'
	>>> booth('abaadabaacabaab')
	'aababaadabaacab'
	"""
	old_length, s = len(s), 2*s
	offset, answer = 0, 0
	# for i in xrange(1, len(s)):  # cannot use old_length here   # cannot modify i like in Java
	while i < len(s):
		"""Actually, this first case should efficiently address 'bbbbbbbbba'"""
		if s[i] < s[answer]:  # equiv to offset == 0 case (but creates efficiency, see note above)
			answer = i  # New lexicographical minimum found.
			offset = 0  # Reset all parameters here
		elif s[i] == s[answer + offset]:
			offset += 1  #  Keep moving the offset till this new string matches the previous answer
		elif s[i] < s[answer + offset]:
			# Some char is found which is lower than the char at same offset in the previous answer. (e.g. 'aba' with 'abb')
			# So new answer becomes the lexicographical minimum, discard the previous answer in favor of the new answer.
			answer = i - offset
			offset = 0
			i = answer   # triggers for ones like 'ababa'  # will start at ans+1, like at base case
			# ^need because arbitrary 'ababa', 'aabaabaaab', 'aaabaaabaaaab'
		else:  
			# In the new match, some char is found which is higher than the char at same offset in the previous answer.
            # So new answer cannot be the lexicographical minimum, discard it.
			offset = 0
		i += 1
	return s[answer : answer + old_length]
     

# Fixed: see note above
# Sieve out just the possible start indices; will address worst case of bbbbbbbbba.  
# However, will not address things like aaaaaaaaab.  Fortunately, booth() can already handle that efficiently.
def booth_indices(s):  
	curr_min = s[0]
	indices = [0]  # changed to set, don't need indexing
	for i, c in enumerate(s, 0):
		if c < curr_min:
			curr_min = s[i]
			indices = [i]
		elif c == curr_min:
			indices.append(i)
		else: pass
	return indices