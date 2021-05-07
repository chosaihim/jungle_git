import sys
input = sys.stdin.readlineimport sys
sys.setrecursionlimit(10**6)

n = int(input())
left = list(map(int, input().split()))
right = list(map(int, input().split()))
dp = [[0 for _ in range(n+1)] for _ in range(n+1)]

for i in range(n-1,-1,-1):
    for j in range(n-1,-1,-1):
        if left[i] > right[j]:
            dp[i][j] = dp[i][j+1] + right[j]
        else:
            dp[i][j] = max(dp[i+1][j], dp[i+1][j+1])
            
        
print(dp[0][0])

# 시간초과
# import sys
# input = sys.stdin.readline
# sys.setrecursionlimit(10**6)

# n = int(input())
# left = list(map(int, input().split()))
# right = list(map(int, input().split()))
# cache = [[0 for _ in range(n)] for _ in range(n)]

# def scores(l_index, r_index):
#     if cache[l_index][r_index]: return cache[l_index][r_index]
#     result = 0
    
#     if left[l_index] > right[r_index]:
#         result = right[r_index]
#         if r_index + 1 < n:
#             result += scores(l_index, r_index+1)
    
#     if l_index + 1 < n:
#         result = max(result, scores(l_index+1, r_index))
#         if r_index + 1 <n:
#             result = max(result, scores(l_index+1, r_index+1))
    
#     cache[l_index][r_index] = result
#     return result 
    
# print(scores(0,0))