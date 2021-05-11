import sys
input = sys.stdin.readline

T = int(input())

def findMinCost(n, files):
    
    dp = [[0] * n for _ in range(n)]
    sum_ = [0] * (n+1)
    for i in range(1,n+1): sum_[i] = sum_[i-1] + files[i-1]
    
    for i in range(1, n):
        for j in range(n - i):
            x = j + i
            dp[j][x] = 10**10
            for k in range(j, x):
                dp[j][x] = min(dp[j][x], dp[j][k] + dp[k + 1][x] + sum_[x+1] - sum_[j])

    return(dp[0][-1])
            

for _ in range(T):
    k = int(input())
    files = list(map(int,input().split()))
    
    print(findMinCost(k, files))


# 2
# 4
# 40 30 30 50
# 15
# 1 21 3 4 5 35 5 4 3 5 98 21 14 17 32