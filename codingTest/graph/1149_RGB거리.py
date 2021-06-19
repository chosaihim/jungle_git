import sys
input = sys.stdin.readline

n = int(input())
dp = [[0]*3 for _ in range(n)]

# 0th dp
dp[0] = list(map(int, input().split()))

for node in range(1,n):
    r,g,b = map(int,input().split())
    
    # R,G,B = 0,1,2
    dp[node][0] = min(dp[node-1][1],dp[node-1][2]) + r
    dp[node][1] = min(dp[node-1][0],dp[node-1][2]) + g
    dp[node][2] = min(dp[node-1][0],dp[node-1][1]) + b
    
print(min(dp[-1]))