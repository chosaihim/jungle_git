import sys
input = sys.stdin.readline

n, m = map(int, input().split())

board = [list(map(int, input().split())) for _ in range(n)]
blue = [0,0]; red = [0,0]; hole = [0,0]

for row in range(n):
    for col in range(m):
        if board[row][col] == 'B':
            board[row][col] = '.'
            blue = [row,col]
        elif board[row][col] == 'R':
            board[row][col] = '.'
            red = [row, col]
            

def move(row, col, dr, dc):
    move = 0
    while board[row+dr][col+dc] != '#':
        if board[row+dr][col+dc] == 'O':
            return 0, 0, 0
        row += dr
        col += dc
        move += 1
    return row, col, move
        
def bfs():
    visit = {}
    queue = deque([red+blue])
    
    
    
# from sys import stdin
# from collections import deque

# n, m = map(int, stdin.readline().split())
# graph = [list(stdin.readline()) for _ in range(n)]
# for i in range(n):
#     for j in range(m):
#         if graph[i][j] == 'R':
#             graph[i][j] = '.'
#             red = [i, j]
#         elif graph[i][j] == 'B':
#             graph[i][j] = '.'
#             blue = [i, j]


# def movemove(x, y, dx, dy):
#     move = 0
#     while graph[x+dx][y+dy] != '#':
#         # 구멍으로 탈출할 경우 0,0 return
#         if graph[x+dx][y+dy] == 'O':
#             return 0, 0, 0
#         x += dx
#         y += dy
#         move += 1
#     return x, y, move

# def bfs():
#     # 빨간 구슬과 파란 구슬 동시에 방문체크 해야함
#     visit = {}
#     queue = deque([red + blue])
#     visit[red[0], red[1], blue[0], blue[1]] = 0
#     while queue:
#         rx, ry, bx, by = queue.popleft()
#         for dx, dy in (-1, 0), (1, 0), (0, -1), (0, 1):      # 상하좌우
#             nrx, nry, rmove = movemove(rx, ry, dx, dy)
#             nbx, nby, bmove = movemove(bx, by, dx, dy)
#             # 두 공 모두 또는 파란 공만 탈출한 경우
#             if not nbx and not nby:
#                 continue
#             # 빨간 공만 탈출한 경우
#             elif not nrx and not nry:
#                 print(visit[rx, ry, bx, by] + 1)
#                 return
#             # 두 공이 같은 위치에 있는 경우
#             elif nrx == nbx and nry == nby:
#                 # 이동거리가 적은 구슬을 한 칸 뒤로
#                 if rmove > bmove:
#                     nrx -= dx
#                     nry -= dy
#                 else:
#                     nbx -= dx
#                     nby -= dy
#             # visit하지 않았으면 queue에 append
#             if (nrx, nry, nbx, nby) not in visit:
#                 visit[nrx, nry, nbx, nby] = visit[rx, ry, bx, by] + 1
#                 queue.append([nrx, nry, nbx, nby])
                
#         # answer에 값을 넣었거나 queue가 비었거나 움직인 횟수가 10이상이면 그만
#         if not queue or visit[rx, ry, bx, by] >= 10:
#             print(-1)
#             return


# bfs() 