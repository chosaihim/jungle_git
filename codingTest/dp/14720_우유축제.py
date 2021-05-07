import sys
input = sys.stdin.readline

n = int(input())
milk = list(map(int, input().split()))

dp =[0] * n
last = -1

if milk[0] == 0: dp[0] = 1; last = 0

for i in range(1,n):
    if (last == milk[i]-1) or (last == milk[i]+2):
            last = milk[i]
            dp[i] = dp[i-1] + 1
    else:
        dp[i] = dp[i-1]
        
print(dp[n-1])