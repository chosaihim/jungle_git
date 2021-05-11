import sys
input = sys.stdin.readline
# sys.setrecursionlimit(10**6)

n = int(input())
milks = [list(map(int, input().split())) for _ in range(n)]
dp = [[[0 for milk_kind in range(3)] for column in range(n)] for _row in range(n)]

d_row = [-1, 0, -1]
d_col = [0, -1, -1]

max_len = 0
if milks[0][0] == 0: dp[0][0][0] = 1

for row in range(n):
    for col in range(n):
        for i in range(3):
            r = row + d_row[i]; c = col + d_col[i]
            
            if 0 <= r < n and 0 <= c < n:
                for m in range(3):
                    if dp[r][c][m] == 0:
                        if milks[row][col] == 0: dp[row][col][0] = max(dp[row][col][0], 1)
                        else: dp[row][col][0] = max(dp[row][col][0], 0)
                    elif m == (milks[row][col]-1) % 3:
                        dp[row][col][milks[row][col]] = max(dp[row][col][milks[row][col]], dp[r][c][m] + 1)
                    else:
                        dp[row][col][m] = max(dp[row][col][m], dp[r][c][m])

    max_len = max(max_len, max(max(dp[row])))


print(max_len)
        
# def drink(n, row, col, milk):
    
#     if row == n-1 and col == n-1: 
#         if milk == milks[row][col]: return 1
#         else: return 0
    
#     d_row = [0,1,1]
#     d_col = [1,0,1]
#     next_milk = (milk + 1)% 3
    
#     count = 0
#     for i in range(3):
#         new_r = row + d_row[i]; new_c = col + d_col[i]
        
#         if new_r < n and new_c < n:
#             if milk == milks[row][col]:
#                 count = max(count, 1+ drink(n, new_r, new_c, next_milk))
#             else:
#                 count = max(count, drink(n, new_r, new_c, milk))
    
#     return count

# print(drink(n,0,0,0))
    
    