import sys
input = sys.stdin.readline

n, m = map(int, input().split())

board = [list(map(int, input().split())) for _ in range(n)]
blue = [0,0]; red = [0,0]; hole = [0,0]

for row in range(n):
    for col in range(m):
        if board[row][col] == 'B':
            blue = [row,col]
        elif board[row][col] == 'R':
            red = [row, col]
        elif board[row][col] == 'O':
            hole = [row,col]
            
def left(B,R,O):
    while B[1] > 0:
        B[1] -= 1
        if board[B[0]][B[1]] == '1':
    
    return

def escape(B,R,O,depth):
    

    True


print(escape(B,R,O,depth))
    
             