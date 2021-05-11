import sys
input = sys.stdin.readline

n = int(input())
matrices = [list(map(int,input().split())) for _ in range(n)]

dp = [[0]*n for _ in range(n)] 

for scope in range(1,n):
    for start in range(n-scope):
        end = start + scope
        dp[start][end] = 2**31
        for middle in range(start, end):
            dp[start][end] = min(dp[start][end], dp[start][middle] + dp[middle+1][end] + matrices[start][0] * matrices[middle][1] * matrices[end][1])
        

print(dp[start][end])