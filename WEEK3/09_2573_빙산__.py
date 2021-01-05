import sys
from collections import deque
input = sys.stdin.readline
sys.setrecursionlimit(10**9)

dr = [-1,0,1,0]
dc = [0,-1,0,1]

#### INPUT ###
R, C = map(int, input().split()) # R = N, C = M
ice = [list(map(int, input().split())) for _ in range(R)]


SPupdated = False
### dfs ####
visited = []
def dfs(row,col):
    global toNextDfs, ice_area, startP, SPupdated
    toNextDfs += 1

    visited.append([row,col])    

    # 물 녹이는 것 먼저
    for i in range(4):
        wr = row + dr[i]; wc = col + dc[i]
        if 0 <= wr < R and 0 <= wc < C:
            if ice[wr][wc] == 0 and ice[row][col] > 0 and [wr,wc] not in visited:
                ice[row][col] -= 1
    
    # 남아있는 빙산 면적 카운트
    if ice[row][col]>0: 
        ice_area += 1
        if not SPupdated:  # 다음 시작 포인트 저장
            SPupdated = True 
            startP[0] = row; startP[1] = col 
    
    # 다음 dfs로 건너가기
    for i in range(4):
        rr = row + dr[i]; cc = col + dc[i]

        if 0 <= rr < R and 0 <= cc < C and ice[rr][cc] > 0 and [rr,cc] not in visited:
            dfs(rr,cc)


### 초기변수값 생성
ice_area = 0            # 현재 빙산이 몇 칸인지 저장
startP = [0,0]          # BFS 시작점
for i in range(R):
    for j in range(C):
        if(ice[i][j]):
            ice_area += 1
            startP[0] = i; startP[1] = j



toNextDfs = 1
pre_left  = 0
year = 0
broken = False

##### MAIN #####
while toNextDfs:
    breakFlag = False
    
    year += 1

    toNextDfs = 0
    pre_left = ice_area
    ice_area = 0
    SPupdated = 0
    visited.clear()    

    ### DFS !!!
    dfs(startP[0],startP[1])
    
    if pre_left > toNextDfs:
        year -= 1
        break
    
    if ice_area == 0:
        if pre_left == 0 or year > 1: year = 0
        break

print(year)