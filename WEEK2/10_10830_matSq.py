import sys
debugFlag = False


def productMatrix(A, B):
    return [[sum(a*b for a, b in zip(A_row,B_col)) for B_col in zip(*B)] for A_row in A]

def matdiv(mat):
    n = len(mat[0])
    for i in range(n):
        for j in range(n):
            mat[i][j] %= 1000   
    return mat


def power(a,b):
    global n
    if(b==0):   return i_mat
    if(b==1):   return a
    else:
        return matdiv(productMatrix(productMatrix(power(a,b//2),power(a,b//2)),power(a,b%2)))




n, b = list(map(int, sys.stdin.readline().split()))
i_mat = [[0 for i in range(n)] for j in range(n)]

for i in range(n):
    for j in range(n):
        if(i == j): i_mat[i][j] = 1
        else: i_mat[i][j] = 0

a = []
for _ in range(n):
    a.append(list(map(int, sys.stdin.readline().split())))

answer = power(a,b)
for i in range(n):
    for j in range(n):
        print(answer[i][j], end=' ')
    print()




