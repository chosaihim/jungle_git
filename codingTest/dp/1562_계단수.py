import sys
input = sys.stdin.readline

n = int(input())

dp = [[0 for _ in range(10)] for _ in range(n+1)] # [0] 자리수 [1] 수
print(dp)

if n < 10:
    print(0)
else:
    dp[10][0] = 1
    for i in range(11,n+1):
        dp[i][0] = dp[i-1][1]
        dp[i][9] = dp[i-1][8]
        
        for j in range(1,9):
            dp[i][j] = dp[i-1][j-1] + dp[i-1][j+1]
            
            
    print(dp)
    # print(sum_dp)
    print(sum(sum_dp))

