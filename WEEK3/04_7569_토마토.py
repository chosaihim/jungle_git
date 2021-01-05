import sys
from collections import deque
input = sys.stdin.readline

############# INPUT
dh = [0,0,0,0,1,-1]
dr = [-1,0,1,0,0,0]
dc = [0,-1,0,1,0,0]

M,N,H = map(int, input().split()) # N:row, M:col, H:height
tomatoes = [[] for _ in range(H)] 
# get input
for h in range(H):
    for row in range(N):
        tomatoes[h].append(list(map(int, input().split())))
# 참고 tomatoes = [[list(map(int, sys.stdin.readline().split())) for _ in range(n)] for _ in range(h)]

# find roots and number of roots
zeros = 0
roots = []
for h in range(H):
    for row in range(N):
        for col in range(M):
            if   tomatoes[h][row][col] == 0: zeros += 1
            elif tomatoes[h][row][col] == 1: roots.append([h,row,col])
            else: pass

emptyFlag = True if len(roots) + zeros == 0 else False

########################################################################

    



def bfs(tomatoes, roots):
    visited = [[[0 for _ in range(M)] for _ in range(N)] for _ in range(H)]     # 방문한 곳을 기록
    depth = [[[0 for _ in range(M)] for _ in range(N)] for _ in range(H)]       # 몇 일 쨰에 방문(익었는지) 표시
    queue = deque()
    global zeros

    for root in roots:
        queue.append(root)                                      # 큐에 시작점을 줄 세움
        depth[root[0]][root[1]][root[2]] = 0

    while queue:                                            # 큐가 빌떄까지 탐색을 계속

        vertex = queue.popleft()        
        h = vertex[0]; r = vertex[1]; c = vertex[2]

        for idx in range(6):
            hh = h + dh[idx]; rr = r + dr[idx]; cc = c + dc[idx]

            if 0 <= hh < H and 0 <= rr < N and 0 <= cc < M and tomatoes[hh][rr][cc] == 0:
                zeros -= 1
                tomatoes[hh][rr][cc] = 1
                queue.append([hh,rr,cc])
                depth[hh][rr][cc] = depth[h][r][c] + 1
    if zeros:
        return -1
    else:
        return max(max(map(max,depth)))

if emptyFlag: print(-1)
else: print(bfs(tomatoes,roots))