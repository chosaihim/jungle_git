#128ms
import sys
input = sys.stdin.readline

n = int(input())
dp = list(map(int, input().split()))

for i in range(1,n): dp[i] = max(dp[i], dp[i-1]+dp[i])
print(max(dp))

# # faster: 84ms
# def find_max(arr, num):
#     if num == 0:
#         return 0
#     tot = arr[0]
#     max_tot = tot
#     for i in range(1, num):
#         if tot > 0 and tot + arr[i] >= 0:
#             tot += arr[i]
#         else:
#             tot = arr[i]
#         if max_tot < tot:
#             max_tot = tot
#     return max_tot

# n = int(input())
# a = list(map(int, input().split()))
# print(find_max(a, n))
