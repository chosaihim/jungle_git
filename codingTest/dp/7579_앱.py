import sys
input = sys.stdin.readline
INF = 10**9

n, m = map(int, input().split())
memory = list(map(int,input().split()))
costs = list(map(int,input().split()))

# 남기는 메모리 기준
#메모리 초과
# dp = [[INF]*(n+1) for _ in range(m+1)]
# dp[0][0] = 0
# for space in range(m+1):
    
#     for m in range(len(memory)):
#         if memory[m] >= space:
#             dp[space][m+1] = min(dp[space][m-1+1],costs[m])
#         else:
#             dp[space][m+1] = min(dp[space-memory[m]][m-1+1]+costs[m], dp[space][m-1])

# print(dp[-1][-1])

# 비용 대비 최대 메모리 기준
max_cost = sum(costs)
dp = [[0]*(n+1) for _ in range(max_cost+1)]

for c in range(1,len(costs)+1):
    if costs[c-1] == 0:
        dp[0][c] = max(dp[0][c-1],memory[c-1])

for cost in range(1,max_cost+1):
    for c in range(1, len(costs)+1):
        if costs[c-1] > cost:
            dp[cost][c] = dp[cost][c-1]
        else:
            dp[cost][c] = max(dp[cost - costs[c-1]][c-1] + memory[c-1], dp[cost][c-1])
    
    if max(dp[cost]) >= m:
        print(cost)
        break      

    