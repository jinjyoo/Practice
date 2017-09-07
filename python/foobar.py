# import math
def answer(n, length=5, s=[]):  # Mutable evaluated once, should not be evaluted more than that
    if not s:
        s.append(''.join(str(num) for num in sieve()))
    return s[0][n : n+length]
    
def sieve(k=20232):  
    """
    https://primes.utm.edu/howmany.html
    https://primes.utm.edu/nthprime/index.php#nth
    ceil((10000+4)-(4*1 + (25-4)*2 + (168-25)*3 + (1229-168)*4) / 5) = 1058 
    -> Sieve should have 1229 + 1058 = 2287 primes long to have enough for 10000
    -> 2287th prime is 20231 (add 1 because of exclusive bound on xrange)
    Could find some f(n) s.t. k = f(n) for better space savings for answer2()
    """
    is_prime = [True]*k 
    for i in xrange(2, k): 
        if is_prime[i]:
            yield i      
        for j in xrange(i*i, k, i):  # important optimization -> start at i*i, since i*2, etc. are already set
            is_prime[j] = False

def answer2(n, length=5):  
    """Assumes this is only called once.  If this will be called multiple times, it'd probably be 
    better to use answer(), which only uses O(n) space and has much simpler logic.
    """
    prime = sieve()
    while n > length:   # In this case, we know that the maximum primes have digits less than length
        n -= num_digits(next(prime))
    s = []
    while n > -length-1:  # don't want n+LENGTH == 0
        k = next(prime)
        s.append(str(k))
        n -= num_digits(k)
    return ''.join(s)[n : n+length]

def num_digits(num):
    # return math.ceil(math.log(num, 10))  # More general but slow
    if num < 10:
        return 1
    elif num < 100:
        return 2
    elif num < 1000:
        return 3
    elif num < 10000:
        return 4
    else:
        return 5

"""Question 2"""
# Feels somewhat janky... Some DP solution, maybe?
def answer(lst):  
    count = [0]*10  # 0 to 9
    for num in lst:
        count[num] += 1
    ones = count[1] + count[4] + count[7]
    twos = count[2] + count[5] + count[8]
    total = (ones + 2*twos) % 3
    if total == 1:
        if ones >= 1:
            decr_one(count, [1, 4, 7])
        elif twos >= 2:
            decr_two(count, [2, 5, 8])
        else:
            return 0
    elif total == 2:
        if twos >= 1:
            decr_one(count, [2, 5, 8])
        elif ones >= 2:
            decr_two(count, [1, 4, 7])
        else:
            return 0
    res = ''.join(str(i)*count[i] for i in xrange(len(count)-1, -1, -1))  
    return int(res) if res else 0  # res could be '' if not any(count)

def decr_one(lst, indexes):  # expects indexes to be sorted
    for idx in indexes:
        if lst[idx] > 0:
            lst[idx] -= 1
            return 

def decr_two(lst, indexes):
    remaining = 2
    for idx in indexes:
        if lst[idx] >= remaining:  # >= 1
            lst[idx] -= remaining
            return  # this should always be reached
        elif lst[idx] == 1:  
            lst[idx] -= 1
            remaining -= 1
