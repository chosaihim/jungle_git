import sys
input = sys.stdin.readline

n = int(input())

dp = [1] * (n+1)
dp[1] = 0

for i in range(4, n+1):
    dp[i] = 1+ min(dp[i//3]+i%3, dp[i//2]+i%2)

print(dp[n])
