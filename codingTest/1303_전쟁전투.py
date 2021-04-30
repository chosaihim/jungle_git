import sys
from collections import deque
input = sys.stdin.readline

#### INPUT ####
n, m = map(int, input().split())

soldiers = [[0 for _ in range(n)] for _ in range(m)]
visited = [[0 for _ in range(n)] for _ in range(m)]     # 방문한 곳을 기록


for row in range(m):
    row_input = input()
    for col in range(n):
        soldiers[row][col] = row_input[col]


drow = [0,1,0,-1]
dcol = [1,0,-1,0]
### BFS
def bfs(soldiers, root):
    counts = 1
    word = soldiers[root[0]][root[1]] 
    queue = deque([root])
    visited[root[0]][root[1]] = 1
    
    while queue:
        row, col = queue.popleft()
        
        for i in range(4):
            r = row + drow[i]; c = col + dcol[i]; 
            if 0<= r < m and 0<= c < n:
                if not visited[r][c] and soldiers[r][c] == word:
                    queue.append([r,c])
                    visited[r][c] = 1
                    counts += 1
    return counts
                

power = [0,0]
for row in range(m):
    for col in range(n):
        if not visited[row][col]:
            size = bfs(soldiers,[row,col])
            if soldiers[row][col] == 'W':
                power[0] += size*size
            else:
                power[1] += size*size

print(power[0],power[1])


# 빠른 정답
# m,n=map(int,input().split())
# g=[[*input()] for i in[0]*n]
# def f(i,j,x):
#     q=[(i,j)];c=1;g[i][j]=0
#     while q:
#         i,j=q.pop()
#         for i,j in [(i+1,j),(i-1,j),(i,j+1),(i,j-1)]:
#             if i>-1 and i<n and j>-1 and j<m and g[i][j]==x:q+=[[i,j]];g[i][j]=0;c+=1
#     return c*c
# B,W=0,0
# for i in range(n):
#     while 'B'in g[i]:B+=f(i,g[i].index('B'),'B')
# for i in range(n):
#     while 'W'in g[i]:W+=f(i,g[i].index('W'),'W')
# print(W,B)