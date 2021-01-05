import sys, math
N,r,c = list(map(int, sys.stdin.readline().split()))


def debug_print(num):
    if num == 0:
        print("[ o x ]")
        print("[ x x ]")
        print("-------")
    elif num == 1:
        print("[ x o ]")
        print("[ x x ]")
        print("-------")
    elif num == 2:
        print("[ x x ]")
        print("[ o x ]")
        print("-------")
    else:
        print("[ x x ]")
        print("[ x o ]")
        print("-------")



def findz(n,y,x,r,c):
    inc = int(math.pow(2,n-1)) #increase

    total_move = 0
    move = 0

    if n==0:
        if(x==c and y==r):
            move = 0
    else:
        if(c< x+inc and r < y+inc):
            # debug_print(0)
            move += 0
            move += findz(n-1,y,x,r,c)
        elif(c< x+2*inc and r<y+inc):
            # debug_print(1)
            move += inc*inc
            move += findz(n-1,y,x+inc,r,c)
        elif(c< x+inc and r<y+2*inc):
            # debug_print(2)
            move += 2*inc*inc
            move += findz(n-1,y+inc,x,r,c)
        elif(c< x+2*inc and r<y+2*inc):
            # debug_print(3)
            move += 3*inc*inc
            move += findz(n-1,y+inc,x+inc,r,c)
    
    total_move += move
    return total_move

print(findz(N,0,0,r,c))
