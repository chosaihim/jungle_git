import sys
from collections import deque
input = sys.stdin.readline

def bfs(start):
    visited = [[0 for _ in range(C)] for _ in range(R)]
    SPupdated = False
    queue=deque([start])
    visited[start[0]][start[1]] = 1
    ice_area,pop_count = 0,0
    point = [-1,-1]
    
    while queue:
        pop_count += 1
        row,col = queue.popleft()
        for idx in range(4):
            wr = row + dr[idx]
            wc = col + dc[idx]
            # if ice[wr][wc] == 0 and ice[row][col] > 0 and not visited[wr][wc]:
            if ice[wr][wc] == 0 and not visited[wr][wc]:
                if ice[row][col] > 0: ice[row][col] -= 1
                
        # 남아있는 빙산 면적 카운트
        if ice[row][col] > 0 :
            ice_area += 1
            point = [row,col]
        
        for idx in range(4):
            wr = row + dr[idx]
            wc = col + dc[idx]
            if ice[wr][wc]  and not visited[wr][wc]:
                queue.append([wr,wc])
                visited[row][col] = 1
                
        # 남아있는 빙산 면적 카운트
        if ice[row][col] > 0 :
            ice_area += 1
            point = [row,col]

    return ice_area, pop_count, point


dr = [-1,0,1,0]
dc = [0,-1,0,1]
R, C = map(int, input().split()) # R = N, C = M
ice = [list(map(int, input().split())) for _ in range(R)]
ice_area = 0            # 현재 빙산이 몇 칸인지 저장
for i in range(R):
    for j in range(C):
        if(ice[i][j]):
            ice_area += 1
            startP = [i,j]

if ice_area == 0:
    print(0)
    exit()
### MAIN
year = 1
while True:
    pre_ice  = ice_area
    ice_area,pop_count,startP = bfs(startP)
    if pre_ice > pop_count:
        break
    if ice_area == 0:
        if pre_ice == 0: year = 0
        elif(year > 1): year = 0
        break
    year += 1
print(year)