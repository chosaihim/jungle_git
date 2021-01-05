import sys
from collections import deque
input = sys.stdin.readline

dx = [-1,0,1,0]
dy = [0,-1,0,1]

R, C = map(int, input().split())
alphabets = [['' for _ in range(C)] for _ in range(R)]

for row in range(R):
    row_input = input()
    for col in range(C):
        alphabets[row][col] = row_input[col]

def dfs(alphabets, root):
    visited = []
    depth = [[0 for _ in range(C)] for _ in range(R)]
    depth[0][0] = 1
    max_depth = 0

    stack = [root]
    
    while stack:
        vertex = stack.pop()
        r = vertex[0]; c = vertex[1]        
        # print(f'vertex:{vertex}, depth:{depth[r][c]}')        


        if(len(visited) >= depth[r][c]):            
            while len(visited) >= depth[r][c]:
                visited.pop()
            # print(visited)

        if alphabets[r][c] not in visited:
            visited.append(alphabets[r][c])

            for i in range(4):
                rr = r + dy[i]; cc = c + dx[i]
                if 0 <= rr < R and 0 <= cc < C:
                    if alphabets[rr][cc] not in visited:
                        depth[rr][cc] = depth[r][c] + 1
                        stack.append([rr,cc])
            
        # print(f'visited:{visited}')
        # print(f'stack:{stack}')

        # for i in range(R):
        #     print(depth[i])
        # print()
        
        max_depth = max(max_depth,depth[r][c])
        
    print(max_depth)
    return max(map(max,depth))

print(dfs(alphabets,[0,0]))