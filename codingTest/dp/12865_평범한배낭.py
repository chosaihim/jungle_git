import time
start_time = time.time()  # 시작 시간 저장

#7952ms 202010514
# import sys
# input = sys.stdin.readline

# n, k = map(int, input().split()) # n: 물품의 수 k: 최대 무게
# items = [list(map(int,input().split())) for item in range(n)]
# # items.sort()

# def knapsack(n, k, items):
#     dp = [[0] * (n+1) for _ in range(k+1)]
    
#     # if items[0][0] > k: return 0
#     # else:
#     for weight in range(1, k+1):
#         for item in range(1, len(items)+1):
#             w, v = map(int,items[item-1])
            
#             if w > weight:
#                 dp[weight][item] = dp[weight][item-1]
#             else:
#                 dp[weight][item] = max(dp[weight][item-1], dp[weight - w][item-1] + v)
    
#     return dp[k][n]

# print(knapsack(n,k,items))



# #4048ms 4달전
# import sys
# input = sys.stdin.readline

### INPUT
# N: 
N, K = map(int, input().split()) # N: number of items, K: maximum wieght K(1 ≤ K ≤ 100,000)
items = [list(map(int, input().split())) for _ in range(N)] # W: 무게 V:가치 [W,V] W(1 ≤ W ≤ 100,000)

def knapsack(N,K,items):
    dp = [[0]*(K+1) for _ in range(N+1)]

    for i in range(1,N+1): # i: item
        weight, value = map(int, items[i-1])
        for j in range(1,K+1): # j:가방에 담을 수 있는 무게
            if weight <= j:
                dp[i][j] = max(dp[i-1][j],dp[i-1][j-weight]+value)
            else:
                dp[i][j] = dp[i-1][j]

    print(dp[N][K])

knapsack(N,K,items)


# 다른 사람 코드
import sys
read = sys.stdin.readline


def dp(n, k):
    dp_dict = {0: 0}
    for _ in range(n):
        new_w, new_v = map(int, read().split())
        temp = {}
        for acc_w, acc_v in dp_dict.items():
            if acc_w + new_w <= k and acc_v + new_v > dp_dict.get(acc_w + new_w, 0):
                temp[acc_w + new_w] = acc_v + new_v
        dp_dict.update(temp)
    return max(dp_dict.values())


N, K = map(int, read().split())
print(dp(N, K))

end_time = time.time()
print("WorkingTime: {} sec".format(end_time-start_time))