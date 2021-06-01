import sys
from collections import deque
input = sys.stdin.readline


T = int(input())

dir = [[1,0],[0,1],[-1,0],[0,-1]]
def bfs(graph, visited, root):
    queue = deque([root])
    visited[root[0]][root[1]] = True
    
    while queue:
        row, col = queue.popleft()
        
        for drow, dcol in dir:
            new_r = row + drow; new_c = col + dcol
            
            if 0 <= new_r < n and 0 <= new_c < m:
                if graph[new_r][new_c] and not visited[new_r][new_c]:
                    visited[new_r][new_c] = True
                    queue.append([new_r, new_c])
            
for test in range(T):
    m, n, k = map(int, input().split())
    
    graph = [[False] * m for row in range(n)]
    visited = [[False] * m for row in range(n)]
    lettuce = []
    count = 0
    
    for i in range(k):
        x, y = map(int, input().split())
        graph[y][x] = True
        lettuce.append([y,x])
    
    for row, col in lettuce:
        if not visited[row][col]:
            count += 1
            bfs(graph, visited, [row,col])

    print(count)