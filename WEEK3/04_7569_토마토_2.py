import sys
from collections import deque
input = sys.stdin.readline

############# INPUT
dh = [0,0,0,0,1,-1]
dr = [-1,0,1,0,0,0]
dc = [0,-1,0,1,0,0]

M,N,H = map(int, input().split()) # N:row, M:col, H:height
tomatoes = [[list(map(int, sys.stdin.readline().split())) for _ in range(N)] for _ in range(H)]

queue = deque()

for h in range(H):
    for row in range(N):
        for col in range(M):
            if tomatoes[h][row][col] == 1: queue.append([h,row,col])

########################################################################


def bfs():
    max_depth = 1

    while queue:                                            # 큐가 빌떄까지 탐색을 계속

        vertex = queue.popleft()        
        h = vertex[0]; r = vertex[1]; c = vertex[2]

        for idx in range(6):
            hh = h + dh[idx]; rr = r + dr[idx]; cc = c + dc[idx]

            if 0 <= hh < H and 0 <= rr < N and 0 <= cc < M and tomatoes[hh][rr][cc] == 0:
                tomatoes[hh][rr][cc] = tomatoes[h][r][c] + 1
                queue.append([hh,rr,cc])
                max_depth = max(max_depth,tomatoes[hh][rr][cc])
        
    return max_depth-1
            


answer = bfs()
for h in range(H):
    for row in range(N):
        for col in range(M):
            if tomatoes[h][row][col] == 0 : answer = -1

print(answer)