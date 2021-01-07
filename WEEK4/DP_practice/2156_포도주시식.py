import sys
input = sys.stdin.readline

n = int(input())
wine = [int(input()) for _ in range(n)]

last = [0,0]
dp = [0]*n
for i in range(n):
    if(i == 0): dp[0] = wine[0]
    elif(i == 1): dp[1] = wine[0] + wine[1]
    elif(i == 2): dp[2] = max(wine[0]+wine[1],wine[1]+wine[2],wine[0]+wine[2])

    else:
        dp[i] = max(dp[i-3]+wine[i-1]+wine[i], dp[i-2]+wine[i], dp[i-1])

print(max(dp))