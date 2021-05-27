import sys
input = sys.stdin.readline
sys.setrecursionlimit(10**6)

n = int(input())

red = [False] * n
blue = [False] * n
count = [0]

board = [['']* n for _ in range(n)]

def printBoard():
    for i in range(n):
        for j in range(n):
            if board[i][j] == 'r':
                print("r", end = '')
            elif board[i][j] == 'b':
                print("b", end = '')
            else:
                print("□", end = '')
        print()


def color(n, row):
    for r_col in range(n):
        if not red[r_col]:
            for b_col in range(n):
                if b_col != r_col:
                    if not blue[b_col]:
                        # board[row][r_col] = 'r'
                        # board[row][b_col] = 'b'
                        red[r_col] = True
                        blue[b_col] = True
                        if row == n-1:
                            # print("--------")
                            # printBoard()
                            count[0] += 1
                        else:
                            color(n,row+1)
                        # board[row][r_col] = ''
                        # board[row][b_col] = ''
                        blue[b_col] = False
                        red[r_col] = False
        
color(n,0)
print(count[0]%1000000007)