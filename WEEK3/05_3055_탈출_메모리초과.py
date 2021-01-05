import sys
from collections import deque
input = sys.stdin.readline

#### INPUT ####
r, c = map(int, input().split())
forest = [list(map(str, input())) for i in range(r)] # . 빈곳, * 물 , X 돌, D 비버굴, S 고슴도치
## END INPUT ##

# 변수세팅
dr = [-1,0,1,0]
dc = [0,-1,0,1]
D=[0,0]; S=[0,0]

q_wat = deque()
# 고슴도치와 비버굴 위치 파악
for row in range(r):
    for col in range(c):
        if   forest[row][col] == 'D': D[0]=row; D[1]=col
        elif forest[row][col] == 'S': S[0]=row; S[1]=col
        elif forest[row][col] == '*': q_wat.append([row,col])


# BFS 함수
def bfs(S):
    global r, c
    forest[S[0]][S[1]] = 0

    queue = deque()                                           # 큐에 시작점을 줄 세움
    queue.append([S[0],S[1],0]) # x, y, depth

    while queue: # 큐가 빌 때 까지 탐색을 계속 
                        
        # 물 확장
        w_run = len(q_wat)
        for _ in range(w_run):
            w_vtx = q_wat.popleft()

            for idx in range(4):
                rr = w_vtx[0] + dr[idx]; cc = w_vtx[1] + dc[idx]

                if 0<= rr < r and 0<= cc < c and forest[rr][cc] != 'X' and forest[rr][cc] != 'D':
                    forest[rr][cc] = -1
                    q_wat.append([rr,cc])

        
        # 고슴도치 이동
        q_len = len(queue)
        for _ in range(q_len):
            
            vertex = queue.popleft()
            # go_r = vertex[0]; go_c = vertex[1]; 
            depth = vertex[2]

            for idx in range(4):
                rr = vertex[0] + dr[idx]; cc = vertex[1] + dc[idx]

                if 0 <= rr < r and 0 <= cc < c:
                    if forest[rr][cc] == 'D' : 
                        return str(depth + 1)
                    elif forest[rr][cc] == '.' :
                        forest[rr][cc] = depth + 1
                        queue.append([rr,cc, depth+1])
    
    return "KAKTUS"

print(bfs(S))