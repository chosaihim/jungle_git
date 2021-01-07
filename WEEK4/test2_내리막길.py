import sys
input = sys.stdin.readline
sys.setrecursionlimit(10**9)

n, m = map(int,input().split())
Map = [list(map(int, input().split())) for _ in range(n)]

d_row = [-1, 0, 1, 0]
d_col = [0, -1, 0, 1]

cache = [[None]*(m+1) for _ in range(n+1)]

def dp(arrive):
    
    arrival_cnt = 0
    cur_row, cur_col = arrive

    if arrive == [n-1,m-1]: return 1
    if cache[cur_row][cur_col] != None: return cache[cur_row][cur_col]
    
    for i in range(4):
        next_row, next_col = cur_row + d_row[i], cur_col + d_col[i]
        if 0 <= next_row < n and 0 <= next_col < m and Map[next_row][next_col] < Map[cur_row][cur_col]:
            arrival_cnt +=  dp([next_row,next_col])
    
    cache[cur_row][cur_col] = arrival_cnt
    return arrival_cnt
            

print(dp([0,0]))

