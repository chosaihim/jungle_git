#5656ms
import sys
input = sys.stdin.readline
from collections import deque

n, m = map(int, input().split())
graph = []
visited = [[[0 for wall in range(2)] for _ in range(m)] for _ in range(n)]
drow = [1, 0, -1, 0]
dcol = [0, 1, 0, -1]


for i in range(n):
    graph.append(list(map(int,list(input().strip()))))
    

def bfs(graph):
    
    queue = deque([[0,0,1,0]])
    visited[0][0][0] = 1

    while queue:
        row, col, depth, wall = deque.popleft(queue)
        
        if [row, col] == [n-1, m-1]: return depth
        
        for dr, dc in zip(drow, dcol):
            r = row + dr; c = col + dc
            
            if 0 <= r < n and 0 <= c < m and not visited[r][c][wall]:
                if graph[r][c] == 1 and wall == 0:
                    deque.append(queue,[r,c,depth+1,1])
                    visited[r][c][1] = 1
                elif graph[r][c] == 0:# and not visited[r][c][wall]:
                    deque.append(queue,[r,c,depth+1,wall])
                    visited[r][c][wall] = 1

    
    return -1

print(bfs(graph))


#2420
# https://www.acmicpc.net/problem/2206
import sys
I = sys.stdin.readline
def bfs(r,c):
    que = [(0,0,False)]
    count = 1
    while que:
        que_ = []
        for r,c,flag in que:
            if r == R-1 and c == C-1:
                return count
            for dr, dc in dir:
                rr = r + dr
                cc = c + dc
                if 0 <= rr < R and 0 <= cc < C:
                    if not flag:
                        if not visitF[rr][cc]:
                            if Map[rr][cc] == '0':
                                visitF[rr][cc] = True
                                que_.append((rr,cc,False))
                            else:
                                visitF[rr][cc] = True
                                que_.append((rr,cc,True))
                    else:
                        if not visitT[rr][cc]:
                            if Map[rr][cc] == '0':
                                visitT[rr][cc] = True
                                que_.append((rr,cc,True))
        
        que = que_
        count += 1
    return -1

dir = [[1,0], [-1,0], [0,1], [0,-1]]
R, C = list(map(int, I().split()))
Map = [list(I()) for _ in range(R)]
visitF = [[False] * C for _ in range(R)]
visitT = [[False] * C for _ in range(R)]

print(bfs(0,0))
