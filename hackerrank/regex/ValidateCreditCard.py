# https://www.hackerrank.com/challenges/validating-credit-card-number/problem

"""
► It must start with a 4, 5 or 6. 
► It must contain exactly 16 digits. 
► It must only consist of digits (-). 
► It may have digits in groups of 4, separated by one hyphen "-". 
► It must NOT use any other separator like ' ' , '_', etc. 
► It must NOT have 4 or more consecutive repeated digits.
"""
import re
pattern = re.compile(r'''
                    ^
                    (?!.*(\d)(-?\1){3})   # no 4+ duplicate digits; {3,} is not necessary           
                    [456]\d{3}        # 4/5/6 + 3 digits
                    (?:-?\d{4}-?){3}  # 3 groups of (optional '-' + 4 digits)
                    $                 # enforce 16 digits  
                    ''', re.X)
'''For the first line (?!...), we need the parentheses around (-?\1), else we fail things like 5133-3367-8912-3456. This is because the - can be anywhere; -3333, 3-333, 33-33, 3-333, 3333-.  This would also allow invalid things like 3-3-3-3, but filtering this will be taken care of in the normal regex.
'''
for _ in range(int(input().strip())):
    print("Valid" if pattern.search(input().strip()) else "Invalid")
    