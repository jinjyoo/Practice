# https://www.hackerrank.com/challenges/validating-the-phone-number/problem

import re
pattern = re.compile(r'[789]\d{9}$')  # 10 digit number that starts with 7|8|9
for _ in range(int(input().strip())):
    number = input().strip()
    match = pattern.match(number)
    print('YES' if match else 'NO')