import sys
from collections import deque
input = sys.stdin.readline

dr = [-1,0,1,0]
dc = [0,-1,0,1]

R, C = map(int, input().split()) # R = N, C = M
ice = [list(map(int, input().split())) for _ in range(R)]
visited = [[0 for _ in range(C)] for _ in range(R)]

queue = deque()
pop_count = 0
# visited = []
def bfs(r,c):

    global ice_area,pop_count
    SPupdated = False

    queue.append([r,c])
    # visited.append([r,c])
    visited[r][c] = 1

    while queue:
        row,col = queue.popleft()
        # pop_count += 1
        visited[row][col] = 1
        print(pop_count)
        for i in range(R): print(visited[i])
        cnt = 0
        for drr,dcc in zip(dr,dc):
            wr = row + drr; wc = col + dcc
            if ice[wr][wc] == 0 and not visited[wr][wc]:
                ice[row][col] -= 1
                # if ice[row][col] > 0 and not visited[wr][wc]:
                    # cnt += 1
                    # ice[row][col] -= 1
        if(ice[row][col]<=0):ice[row][col] = 0
        else: ice_area += 1; #x = row; y=col
        
        # # 남아있는 빙산 면적 카운트
        # if ice[row][col] > 0 : 
        #     ice_area += 1
        #     startP[0] = row; startP[1] = col
        
        # for idx in range(4):
        #     rr = row + dr[idx]; cc = col + dc[idx]
            
        for drr,dcc in zip(dr,dc):
            rr = row + drr; cc = col + dcc
            if ice[rr][cc]> 0:
                if not visited[rr][cc] and [rr,cc] not in queue:
                    queue.append([rr,cc])
                    pop_count += 1
                

            


# for row in range(R): print(ice[row])


### 초기변수값 생성
ice_area = 0            # 현재 빙산이 몇 칸인지 저장
# startP = [0,0]          # BFS 시작점
x = 0; y = 0
for i in range(R):
    for j in range(C):
        if(ice[i][j]):
            ice_area += 1
            # startP[0] = i; startP[1] = j
            x = i; y = j



### MAIN
year = 0
while ice_area:
    
    pre_ice   = ice_area
    ice_area  = 0
    pop_count = 1
    # visited.clear()
    visited = [[0 for i in range(C)] for j in range(R)]

    bfs(x,y)
    
    # for i in range(R):
    #     for j in range(C):
    #         if(ice[i][j]):
    #             ice_area += 1
    #             x = i; y = j
    
                
    print(f'popCount:{pop_count}, pre_ice:{pre_ice}, ice_area:{ice_area}')
    for i in range(R): print(ice[i])

    if pre_ice > pop_count: break    
    if ice_area == 0: year = 0; break
    if pre_ice < pop_count: break
    year += 1

print(year)


#print(f'popCount:{pop_count}, ice_area:{ice_area}')
# print("***************************")
# for row in range(R): print(ice[row])


