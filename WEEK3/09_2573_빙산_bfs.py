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

    while queue:                                            # 큐가 빌떄까지 탐색을 계속
        # print(queue)
        # print(visited)
        vertex = queue.popleft()
        pop_count += 1
        row = vertex[0]; col = vertex[1]
        # visited.append([row,col])
        visited[row][col] = 1

        for idx in range(4):
            wr = row + dr[idx]; wc = col + dc[idx]
            # if 0 <= wr < R and 0 <= wc < C:
            # if ice[wr][wc] == 0 and ice[row][col] > 0 and [wr,wc] not in visited:
            if ice[wr][wc] == 0 and ice[row][col] > 0 and not visited[wr][wc]:
                ice[row][col] -= 1
        
        # 남아있는 빙산 면적 카운트
        if ice[row][col] > 0 : 
            ice_area += 1
            if not SPupdated: startP[0] = row; startP[1] = col
        
        for idx in range(4):
            rr = row + dr[idx]; cc = col + dc[idx]
            # if 0 <= rr < R and 0 <= cc < C:
            # if ice[rr][cc]> 0 and [rr,cc] not in visited and [rr,cc] not in queue:
                # queue.append([rr,cc])
            if ice[rr][cc]> 0 and not visited[rr][cc] and [rr,cc] not in queue:
                queue.append([rr,cc])
                

            


# for row in range(R): print(ice[row])


### 초기변수값 생성
ice_area = 0            # 현재 빙산이 몇 칸인지 저장
startP = [0,0]          # BFS 시작점
for i in range(R):
    for j in range(C):
        if(ice[i][j]):
            ice_area += 1
            startP[0] = i; startP[1] = j
            break



### MAIN
year = 0
while ice_area:

    year += 1
    
    pre_ice   = ice_area
    ice_area  = 0
    pop_count = 0
    # visited.clear()
    for i in range(R):
        for j in range(C):
            if visited[i][j] != 0: visited[i][j] = 0

    bfs(startP[0],startP[1])
    
    # print(f'popCount:{pop_count}, ice_area:{ice_area}')

    if pre_ice > pop_count:
        year -= 1
        break
    
    if ice_area == 0:
        if pre_ice == 0: year = 0
        elif(year > 1): year = 0
        break

print(year)


#print(f'popCount:{pop_count}, ice_area:{ice_area}')
# print("***************************")
# for row in range(R): print(ice[row])
