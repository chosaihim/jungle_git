import sys
from collections import deque
input = sys.stdin.readline

dr = [-1,0,1,0]
dc = [0,-1,0,1]

R, C = map(int, input().split())
alphabets = [['' for _ in range(C)] for _ in range(R)]

for row in range(R):
    row_input = input()
    for col in range(C): alphabets[row][col] = row_input[col]

visited = [0 for _ in range(26)]
max_depth = 0
depth = 0
def dfs(row,col,depth):
    # print(f'row:{row}, col:{col}, depth:{depth}')

    # visited.append(alphabets[row][col])
    # print(f'visited:{visited}')
    visited[ord(alphabets[row][col])-65] = 1
    # print(visited)

    global max_depth

    max_depth = max(max_depth,depth)

    for i in range(4):
        rr = row + dr[i]; cc = col + dc[i]
        if 0 <= rr < R and 0 <= cc < C:
            # if alphabets[rr][cc] not in visited:
            if visited[ord(alphabets[rr][cc])-65] == 0:
                dfs(rr,cc,depth+1)
                visited[ord(alphabets[rr][cc])-65] = 0
                # visited.pop()
                
dfs(0,0,1)
print(max_depth)