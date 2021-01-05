import sys, math
n = int((sys.stdin.readline().split())[0])
# n = 3
cnt = 0

check = [[0 for i in range(n)] for j in range(n)] # 못 놓으면 >1 놓을수 있으면 0

check_row = [0 for i in range(n)]
check_col = [0 for i in range(n)]
check_rd  = [0 for i in range(2*n-1)]
check_ld  = [0 for i in range(2*n-1)]


def printcheck():
    for i in range(len(check[0])):
        print(check[i])

def ccheck(n:int, row:int, col:int):
    for i in range(n):
        for j in range(n):
            if(i == row or j == col or (i+j) == (row + col) or (i-j) == (row - col)):
                check[i][j] += 1

def uncheck(n:int, row:int, col:int):
    
    for i in range(n):
        for j in range(n):
            if(i == row or j == col or (i+j) == (row + col) or (i-j) == (row - col)):
                check[i][j] -= 1

def checking(n, row, col, mode):
    check_row[row] += mode
    check_col[col] += mode
    check_rd[row+col] += mode
    check_ld[col-row + n-1] += mode

def nq(n:int, col:int):
    global cnt

    if(col == n):
        cnt += 1
    else:
        for i in range(n):
            # if check[i][col] == 0:
            #     ccheck(n, i,col)
            #     nq(n,col+1)
            #     uncheck(n, i,col)
            if not (check_row[i] or check_col[col] or check_rd[i+col] or check_ld[col-i+n-1]):
                checking(n,i,col,1)
                # printcheck()
                nq(n,col+1)
                checking(n,i,col,-1)
                # printcheck()
            else: continue
    return cnt

nq(n,0)
print(cnt)


