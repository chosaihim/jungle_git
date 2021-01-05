import sys
input = sys.stdin.readline

n = int(input())
Palindrome = list(input().split())

# print(Palindrome)

answer = 1
for i in range(1,n):
    if Palindrome[i-1][-1] == Palindrome[i][0]: answer = 1
    else: answer = 0; break

print(answer)
