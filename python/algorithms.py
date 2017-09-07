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