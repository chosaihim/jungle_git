# https://www.acmicpc.net/problem/14501
# 정답보고 품
import sys
input = sys.stdin.readline

n = int(input())
t = []
p = []
for i in range(n):
    t_, p_ = map(int, input().split())
    t.append(t_); p.append(p_)

dp = [0] * (n+1)
for i in range(n):
    if i + t[i] - 1 < n:
        dp[i] = p[i]

for i in range(n-1, -1, -1):
    if i + t[i] > n: dp[i] = dp[i+1]
    else:
        dp[i] = max(dp[i] + dp[i+t[i]], dp[i+1])
    
print(dp[0])
    