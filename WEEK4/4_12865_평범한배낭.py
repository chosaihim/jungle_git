import sys
input = sys.stdin.readline
sys.setrecursionlimit(10**9)


### INPUT
N, K = map(int, input().split()) # N: number of items, K: maximum wieght K(1 ≤ K ≤ 100,000)
items = [list(map(int, input().split())) for _ in range(N)] # W: 무게 V:가치 [W,V] W(1 ≤ W ≤ 100,000)

dp = [[0]*(K+1) for _ in range(N+1)]

for i in range(1,N+1): # i: item
    weight, value = map(int, items[i-1])
    for j in range(1,K+1): # j:가방에 담을 수 있는 무게
        if weight <= j:
            dp[i][j] = max(dp[i-1][j],dp[i-1][j-weight]+value)
        else:
            dp[i][j] = dp[i-1][j]

print(dp[N][K])

