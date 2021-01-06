import sys
input = sys.stdin.readline
# sys.setrecursionlimit(10**6)

n = int(input()) # 1 <= n <= 100

dp = [[0] * (n+1) for _ in range(10)]


for num in range(1,10): dp[num][1] = 1

for digit in range(2, n+1):
    for num in range(10):
        if num == 0: dp[0][digit] = dp[1][digit-1]
        elif num == 9: dp[9][digit] = dp[8][digit-1]
        else: dp[num][digit] = dp[num-1][digit-1] + dp[num+1][digit-1]

answer = 0
for i in range(10):
    # print(dp[i])
    answer += dp[i][n]
    
print(answer% 10**9)