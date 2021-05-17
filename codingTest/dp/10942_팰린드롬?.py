# https://www.acmicpc.net/problem/10942

#2444ms

import sys
input = sys.stdin.readline

n = int(input())
numbers = list(map(int, input().split()))
m = int(input())

#dp
dp = [[0] * n for _ in range(n)]
for i in range(n):
    dp[i][i] = 1

for num_len in range(n):
    for start in range(n - num_len):
        end = start + num_len
        if start == end:
            dp[start][end] = 1
        elif numbers[start] == numbers[end]:
            if start + 1 == end: dp[start][end] = 1
            elif dp[start+1][end-1] == 1: dp[start][end] = 1
            
            
for question in range(m):
    s, e = map(int, input().split())
    
    print(dp[s-1][e-1])

    
# 1596ms
# import sys
# input = sys.stdin.readline
# n = int(input())
# li = list(map(int, input().split()))
# m = int(input())
# palindrome = [-1 for i in range(2*n)]
# for i in range(m):
#     x, y = map(int, input().split())
#     k = x + y - 2
#     t = y - x
#     if palindrome[k] != -1:
#         if palindrome[x+y-2] > t:
#             print(1)
#             continue
#         else:
#             print(0)
#             continue
#     ret = (k+1) % 2
#     for j in range((k+1)//2 - 1, -1, -1):
#         if k-j >= n:
#             break
#         else:
#             if li[j] != li[k-j]:
#                 break
#             else:
#                 ret += 2
#     palindrome[k] = ret
#     if ret > t:
#         print(1)
#     else:
#         print(0)

# 참고
def longest_palindrom(s):
    # 함수를 완성하세요
    return len(s) if s[::-1] == s else max(longest_palindrom(s[:-1]), longest_palindrom(s[1:]))