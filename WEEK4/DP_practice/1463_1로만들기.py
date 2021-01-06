import sys
input = sys.stdin.readline

n = int(input())

dp = [1] * (n+1)
dp[1] = 0

for i in range(1, n+1):

    calc1 = calc2 = calc3 = 10**10
    if not i % 3: calc1 = dp[i//3]
    if not i % 2: calc2 = dp[i//2]
    calc3 = dp[i-1]

    dp[i] = 1 + min(calc1, calc2, calc3)

print(dp[n])
