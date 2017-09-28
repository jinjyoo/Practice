"""
123123, 121232, 552523, 525313
What about cases like 10121?  Could handle with something like r'(?!\d*(\d)\d\5\d\5)'
"""
def solution2():   # Doesn't use regex
    s = input()
    print(s.isdigit() and 100000 <= int(s) <= 999999 and 
          sum([s[i] == s[i+2] for i in range(0, 4)]) < 2)

import re   # Unfortunately, cannot use backreferences in a character class
# Mistakes: should not have anchors at ^ and $.  (?!\1) does not consume anything, need \d afterward for 1 digit.
# Needed a separate case for things like 1515, only covered non-overlapping, like 151 131  
first_pattern = r'^(?!(\d)(?!\1)\1\d*(\d)(?!\2)\2)[1-9]\d{5}$' 
# Mistake: should have \d* at beginning and end so that the first alt. digit pair doesn't have to be at beginning
# Technically don't need the second \d*, since we can stop checking at that point
second_pattern = r'(?!(\d)(?!\1)\d\1\d*(\d)(?!\2)\d\2|(\d)(?!\3)(\d)\3\4)[1-9]\d{5}'
# Mistake: was overcomplicating things the whole time, since 0000 counts as alternating digits.  In other words,
# we don't have to check that for every digit, the following digit is different.  Also, need ^/$ after all, not 
# for the negative lookahead, but for the actual string itself.  
third_pattern = r'(?!\d*(\d)(?!\1)\d\1\d*(\d)(?!\2)\d\2|\d*(\d)(?!\3)(\d)\3\4)[1-9]\d{5}'

# Could use '.' instead of \d for lookahead, since digit check is done anyway in main regex
pattern = re.compile(r'''
                    ^       
                    (?!
                        \d*(\d)(\d)\1\2             # first alt. pair; handles e.g. 1515, 10101 (->1010)
                        |
                        \d*(\d)\d\3\d*(\d)\d\4      # second alt. pair; handles e.g. 101202
                    )
                    [1-9]\d{5}                      # 100000-999999
                    $
                    ''', re.X)
print(re.search(pattern, input()) is not None)      # match() is faster, and makes the ^ redundant
# print(re.search((r'^(?!\d*(\d)(\d)\1\2|\d*(\d)\d\3\d*(\d)\d\4)[1-9]\d{5}$', input()) is not None)
