import sys
input = sys.stdin.readline

n = int(input())
k = int(input())
dp = [[0]*(k+1) for _ in range(n+1)]

# dp 초기화
for i in range(n+1):
    dp[i][0] = 1
    dp[i][1] = i

for total in range(2,n+1):
    for selected in range(2, k+1):
        if total == n:
            dp[total][selected] = dp[total-1][selected] + dp[total-3][selected-1]
        else:
            dp[total][selected] = dp[total-1][selected] + dp[total-2][selected-1]

print(dp[n][k]%1000000003)

# 정답코드
# import sys
# input = sys.stdin.readline
# mod = 1000000003
# n = int(input())
# k = int(input())
# dp = [[0]*(k+1) for _ in range(n+1)]


# for i in range(n+1):
#     dp[i][1] = i
#     dp[i][0] = 1
    
# for i in range(2, n+1):
#     for j in range(2, k+1):
#         if i == n:
#             dp[i][j] = dp[i-3][j-1] + dp[i-1][j]
#         else:
#             dp[i][j] = dp[i-1][j] + dp[i-2][j-1]
#         dp[i][j] %= mod
# print(dp[n][k])