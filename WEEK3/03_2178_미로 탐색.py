import sys
from collections import deque
input = sys.stdin.readline

n, m = map(int, input().split())

mazeMap = [[0 for _ in range(m)] for _ in range(n)]

for row in range(n):
    row_input = input()
    for col in range(len(row_input)-1):
        mazeMap[row][col] = row_input[col]


def bfs(mazeMap, root):
    visited = [[0 for _ in range(m)] for _ in range(n)]     # 방문한 곳을 기록
    depth   = [[0 for _ in range(m)] for _ in range(n)]     # 처음 방문한 순간에 depth(?)가 얼마인지 기록
    depth[0][0] = 1

    queue     = [root]                                      # 큐에 시작점을 줄 세움
    while queue:                                            # 큐가 빌떄까지 탐색을 계속
        vertex = queue.pop(0)

        if vertex [0] == n-1 and vertex[1] == m-1: break    # 마지막 점에 도착했으면 break

        if not visited[vertex[0]][vertex[1]]:               # 꼭지점에 방문한 적 없다면 방문 기록에 추가
            r = vertex[0]; c = vertex[1]
            visited[r][c] = 1

            if r-1 >= 0 and mazeMap[r-1][c]=='1' and depth[r-1][c] == 0: depth[r-1][c] = depth[r][c]+1; queue.append([r-1,c])
            if r+1 <  n and mazeMap[r+1][c]=='1' and depth[r+1][c] == 0: depth[r+1][c] = depth[r][c]+1; queue.append([r+1,c])
            if c-1 >= 0 and mazeMap[r][c-1]=='1' and depth[r][c-1] == 0: depth[r][c-1] = depth[r][c]+1; queue.append([r,c-1])
            if c+1 <  m and mazeMap[r][c+1]=='1' and depth[r][c+1] == 0: depth[r][c+1] = depth[r][c]+1; queue.append([r,c+1])
            
    return depth[n-1][m-1]

print(bfs(mazeMap,[0,0]))