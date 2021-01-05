import sys
from collections import deque
input = sys.stdin.readline

##### INPUT #####
r, c = map(int, input().split())
forest = [list(map(str, input())) for i in range(r)] # . 빈곳, * 물 , X 돌, D 비버굴, S 고슴도치
### END INPUT ###

# 변수세팅
dr = [-1,0,1,0]
dc = [0,-1,0,1]
S  = [0,0]
queue = deque()


for row in range(r):
    for col in range(c):
        if forest[row][col]   == 'S': S[0]=row; S[1]=col            # 고슴도치와 위치 파악
        elif forest[row][col] == '*': queue.append([row,col,-1])    # 현재 물 위치 파악 후 queue에 미리 넣어주기

# BFS 함수
def bfs(S):
    global r, c
    forest[S[0]][S[1]] = 0                                         
    queue.append([S[0],S[1],0]) # x, y, depth # 큐에 시작점을 줄 세움

    while queue: # 큐가 빌 때 까지 탐색을 계속 

        vertex = queue.popleft()

        # 물 확장
        if vertex[2] == -1:
            
            for idx in range(4):
                rr = vertex[0] + dr[idx]; cc = vertex[1] + dc[idx]

                if 0<= rr < r and 0<= cc < c and forest[rr][cc] != 'X' and forest[rr][cc] != 'D' and forest[rr][cc] != -1:
                    forest[rr][cc] = -1
                    queue.append([rr,cc,-1])

        # 고슴도치 이동
        elif vertex[2] >= 0:

            depth = vertex[2]

            for idx in range(4):
                rr = vertex[0] + dr[idx]; cc = vertex[1] + dc[idx]
                
                if 0 <= rr < r and 0 <= cc < c:
                    if forest[rr][cc] == 'D' : 
                        return str(depth + 1)
                    elif forest[rr][cc] == '.' :
                        forest[rr][cc] = depth + 1
                        queue.append([rr,cc, depth+1])
        
        # print(queue)
    return "KAKTUS"    

print(bfs(S))