#5656ms
import sys
input = sys.stdin.readline

n, m = map(int, input().split())
graph = []
visitedF = [[False]*m for _ in range(n)]
visitedT = [[False]*m for _ in range(n)]

delta = [[1,0],[0,1],[-1,0],[0,-1]]

for i in range(n):
    graph.append(list(input().strip()))
    

def bfs(graph):
    
    queue = [(0,0,False)]
    
    visitedF[0][0] = True
    count = 1

    while queue:
        
        que = []
        
        for row, col, wall in queue:
        
            if row == n-1 and col ==  m-1: return count
            
            for dr, dc in delta:
                r = row + dr; c = col + dc
            
                if 0 <= r < n and 0 <= c < m:
                    if wall:
                        if not visitedT[r][c] and graph[r][c] == '0':
                            que.append((r,c,True))
                            visitedT[r][c] = True
                        
                    else:
                        if not visitedF[r][c]:
                            if graph[r][c] == '0':
                                que.append((r,c,False))
                            else:
                                que.append((r,c,True))
                            visitedF[r][c] = True

        queue = que
        count += 1
    return -1

print(bfs(graph))


#2420
# https://www.acmicpc.net/problem/2206
# import sys
# I = sys.stdin.readline
# def bfs(r,c):
#     que = [(0,0,False)]
#     count = 1
#     while que:
#         que_ = []
#         for r,c,flag in que:
#             if r == R-1 and c == C-1:
#                 return count
#             for dr, dc in dir:
#                 rr = r + dr
#                 cc = c + dc
#                 if 0 <= rr < R and 0 <= cc < C:
#                     if not flag:
#                         if not visitF[rr][cc]:
#                             if Map[rr][cc] == '0':
#                                 visitF[rr][cc] = True
#                                 que_.append((rr,cc,False))
#                             else:
#                                 visitF[rr][cc] = True
#                                 que_.append((rr,cc,True))
#                     else:
#                         if not visitT[rr][cc]:
#                             if Map[rr][cc] == '0':
#                                 visitT[rr][cc] = True
#                                 que_.append((rr,cc,True))
        
#         que = que_
#         count += 1
#     return -1

# dir = [[1,0], [-1,0], [0,1], [0,-1]]
# R, C = list(map(int, I().split()))
# Map = [list(I()) for _ in range(R)]
# visitF = [[False] * C for _ in range(R)]
# visitT = [[False] * C for _ in range(R)]

# print(bfs(0,0))