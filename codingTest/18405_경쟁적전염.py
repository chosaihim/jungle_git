#168ms
import sys
from collections import deque
input = sys.stdin.readline

n, k = map(int, input().split())
examiner = [list(map(int, input().split())) for _ in range(n)]
s, x, y = map(int, input().split())

dr = [0, -1, 0, 1]
dc = [-1, 0, 1, 0]

def spread(examiner, k, s):
    
    # 초기 queue 세팅
    virus = [[] for _ in range(k+1)]
    for row in range(n):
        for col in range(n):
            if examiner[row][col]: virus[examiner[row][col]].append([row,col])
    
    queue = deque()
    for i in range(1,k+1):
        for j in range(len(virus[i])):
            queue.append([virus[i][j][0],virus[i][j][1]])
    
    #BFS
    for time in range(s):        
        temp_queue = deque()
        while queue:
            row, col = queue.popleft()
            
            for i in range(4):
                r = row + dr[i]; c = col + dc[i]
                if 0 <= r < n and 0 <= c < n:
                    if examiner[r][c] == 0: 
                        examiner[r][c] = examiner[row][col]
                        temp_queue.append([r,c])
        
        
        for temp in temp_queue:
            queue.append(temp)
    
    return examiner
    

print(spread(examiner, k, s)[x-1][y-1])


#72ms
# import sys
# input = sys.stdin.readline

# def solution():
#     n, k = map(int, input().split())
#     maps = [(list(map(int, input().split()))) for _ in range(n)]
#     s, x, y = map(int, input().split())

#     dx = [-1, 0, 1, 0]
#     dy = [0, 1, 0, -1]

#     x -= 1
#     y -= 1
#     if maps[x][y] != 0 :
#         print(maps[x][y])
#         return
    
#     q = []
#     visited = [(x, y)]
#     maps[x][y] = 1001
#     for i in range(s):
#         temp = []
#         while visited:
#             x, y = visited.pop()
#             for d in range(4):
#                 nx = x+dx[d]
#                 ny = y+dy[d]
#                 if nx > -1 and ny > -1 and nx < n and ny < n:
#                     if maps[nx][ny] != 0 and maps[nx][ny] != 1001:
#                         q.append(maps[nx][ny])
#                     elif maps[nx][ny] == 0:
#                         temp.append((nx, ny))
#                     maps[nx][ny] = 1001
#         visited = temp[:]
#         if q :
#             print(min(q))
#             return
#     if not q :
#         print(0)

# solution()

