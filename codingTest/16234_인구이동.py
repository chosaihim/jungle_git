import sys
from collections import deque
input = sys.stdin.readline

N,L,R = map(int,input().split())
population = [list(map(int, input().split())) for _ in range(N)]

visited = [[0]*N for _ in range(N)]

d_row = [0, 1, 0, -1]
d_col = [1, 0, -1, 0]

def bfs(population, x, y):
    root = [x,y]
    queue = deque([root])
    union = deque()
    
    total = 0
    count = 0
    while queue:
        row, col = queue.popleft()
        union.append([row,col])
        visited[row][col] = 1
        
        total += population[row][col]
        count += 1
        
        for i in range(4):
            r = row + d_row[i]; c = col + d_col[i]
            if 0<= r < N and 0 <= c < N:
                if visited[r][c] == 0 and L <= abs(population[r][c]-population[row][col]) <= R:
                    visited[r][c] = 1
                    queue.append([r,c])
        

    avg = total // count
    for u in union:
        population[u[0]][u[1]] = avg
    
    if count == 1: return False
    else: return True


day = 0
while True:
    immigrantFlag = False
    count = 0
    
    for row in range(N):
        for col in range(N):
            visited[row][col] = 0
            
    for row in range(N):
        for col in range(N):
            if not visited[row][col]:
                bfs(population, row, col)
                count += 1
                # if bfs(population, row, col):
                    # immigrantFlag = True
                
    # if immigrantFlag: day += 1
    # else: break
    # print(count)
    if count == N*N: break
    else: day += 1

print(day)