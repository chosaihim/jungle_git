import sys
input = sys.stdin.readline

# 1,000,000,007

n = int(input())

red = [False] * n
blue = [False] * n
count = [0]

def printRow(red, blue, n):
    for i in range(n):
        if i == red:
            print("r", end = '')
        elif i == blue:
            print("b", end = '')
        else:
            print("x", end = '')
    print()

def color(n, row):
    print(row)
    for r_col in range(n):
        if not red[r_col]:
            red[r_col] = True
            for b_col in range(n):
                if b_col != r_col:
                    if not blue[b_col]:
                        blue[b_col] = True
                        printRow(r_col, b_col, n)
                        if row == n-1:
                            print("--------")
                            count[0] += 1
                        else:
                            color(n,row+1)
                            blue[b_col] = False
            red[r_col] = False
            

color(n,0)
print(count[0])