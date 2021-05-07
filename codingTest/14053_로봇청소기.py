import sys
input = sys.stdin.readline
from collections import deque

n, m = map(int,input().split()) #n:세로 m:가로
r, c, d = map(int, input().split())
space = [list(map(int, input().split())) for _ in range(n)]

# ori_r = [1,0,-1,0]
# ori_c = [0,1,0,-1]
ori_r = [-1,0,1,0]
ori_c = [0,1,0,-1]


def bfs(r, c, d):
    
    root = [r, c, d]
    # queue = deque([root])
    space[r][c] = 2
    count = 1
    row = r; col = c; ori = d;
    
    # while queue:
        # row, col, ori= queue.popleft()
    while True:    
        new_ori = (ori + 3) % 4
        new_row = row + ori_r[new_ori]; new_col = col+ ori_c[new_ori]
    
        if space[new_row][new_col] == 0:
            space[new_row][new_col] = 2
            # queue.append([new_row, new_col, new_ori])
            row = new_row; col = new_col; ori = new_ori
            count += 1
        
        elif space[row+1][col] != 0 and space[row-1][col] != 0 and space[row][col+1] != 0 and space[row][col-1] != 0:
            if space[row-ori_r[ori]][col-ori_c[ori]] != 1:
                # queue.append([row-ori_r[ori], col-ori_c[ori], ori])
                row = row - ori_r[ori]; col = col-ori_c[ori];
            else: 
                break
        
        # elif space[new_row][new_col] != 0:
        else:
            # queue.append([row, col, new_ori])
            ori = new_ori
        
    return count

print(bfs(r,c,d))
        
            
            
        
        
        