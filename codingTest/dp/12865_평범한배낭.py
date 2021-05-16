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


# 가방싸기 함수
def knapsack(N,K,items):
    dp = [[0]*(K+1) for _ in range(N+1)]

    # 가방에 담을 수 있는 물건의 개수를 1개부터 하나씩 늘려 나간다
    for i in range(1,N+1): # i: item
        weight, value = map(int, items[i-1])
        # 가방에 담을 수 있는 최대 무게를 1부터 차례대로 증가시켜 나가면서
        for j in range(1,K+1): # j:가방에 담을 수 있는 무게
            # 현재 물건이 가방이 담을 수 있는 무게보다 적으면 넣어보고 가치를 판단한다
            if weight <= j:
                # 현재 물건을 넣지 않았을 때와 현재 물건을 넣었을 때의 가치를 비교한다.
                dp[i][j] = max(dp[i-1][j],dp[i-1][j-weight]+value)
            # 크면 이 물건을 담지 않고 이전 물건까지 담았을 때 가방에 담을 수 있는 최고 가치를 저장
            else:
                dp[i][j] = dp[i-1][j]

    # 가방에 담을 수 있는 최대 무게에서 모든 물건을 고려했을 때의 최대값을 출력
    print(dp[N][K])



# N: 물건 개수 K:가방에 담을 수 있는 최대 무게
N, K = map(int, input().split())
# 각 물건의 무게와 가치
items = [list(map(int, input().split())) for _ in range(N)] 
# 주어진 조건으로 가방싸기!
knapsack(N,K,items)


# 다른 사람 코드
# import sys
# read = sys.stdin.readline


# def dp(n, k):
#     dp_dict = {0: 0}
#     for _ in range(n):
#         new_w, new_v = map(int, read().split())
#         temp = {}
#         for acc_w, acc_v in dp_dict.items():
#             if acc_w + new_w <= k and acc_v + new_v > dp_dict.get(acc_w + new_w, 0):
#                 temp[acc_w + new_w] = acc_v + new_v
#         dp_dict.update(temp)
#     return max(dp_dict.values())


# N, K = map(int, read().split())
# print(dp(N, K))

end_time = time.time()
print("WorkingTime: {} sec".format(end_time-start_time))