#68ms
import sys
input = sys.stdin.readline

s = input().split('\n')[0]

def is_palindrome(s):
    for i in range(len(s) // 2):
        if not s[i] == s[-i-1]:
            return False
    return True

for i in range(len(s)):
    if(is_palindrome(s[i:len(s)])):
        print(i+len(s))
        break