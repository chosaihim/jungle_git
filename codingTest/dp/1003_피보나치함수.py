import sys
input = sys.stdin.readline

N = int(input())

# def fibonacci(n):
#     if n == 0:
#         answer[0] += 1
#         return 0
#     elif n == 1:
#         answer[1] += 1
#         return 1
#     else:
#         return fibonacci(n-1) + fibonacci(n-2)

for _ in range(N):
    n = int(input())
    
    # answer = [0,0]
    # fibonacci(n)
    # print(answer[0], answer[1])
    
    dp = [[0] * 2 for _ in range(n+1)]
    
    dp[0][0] = 1
    if n > 0:
        dp[1][0] = 0
        dp[1][1] = 1
    if n > 1:
        for i in range(2,n+1):
            for j in range(2):
                dp[i][j] = dp[i-2][j] + dp[i-1][j]
    
    print(dp[n][0],dp[n][1])
    