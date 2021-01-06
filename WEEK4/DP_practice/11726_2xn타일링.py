import sys
input = sys.stdin.readline

n = int(input())

# dp array
dp = [0] * 1001

for i in range(1,n+1):
    if i == 1: dp[1]=1
    elif i == 2: dp[2]=2
    else: dp[i] = (dp[i-1] + dp[i-2]) % 10007

print(dp[n])

# d = [0] * (n+1)
# def dp(x):
#     if x == 1: return 1
#     if x == 2: return 2
#     if(d[x] != 0): return d[x]
    
#     d[x] = (dp(x-2) + dp(x-1))%10007
#     return d[x]

# print(dp(n))

