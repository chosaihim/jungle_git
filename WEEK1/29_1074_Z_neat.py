import sys, math
N,r,c = list(map(int, sys.stdin.readline().split()))

def findz(n,y,x,r,c):
    inc = int(math.pow(2,n-1)) #increase
    move = 0

    if n==0:
        if(x==c and y==r):
            move = 0
    else:
        if(c< x+inc and r < y+inc):
            move += 0
            move += findz(n-1,y,x,r,c)
        elif(c< x+2*inc and r<y+inc):
            move += inc*inc
            move += findz(n-1,y,x+inc,r,c)
        elif(c< x+inc and r<y+2*inc):
            move += 2*inc*inc
            move += findz(n-1,y+inc,x,r,c)
        elif(c< x+2*inc and r<y+2*inc):
            move += 3*inc*inc
            move += findz(n-1,y+inc,x+inc,r,c)
    
    return move

print(findz(N,0,0,r,c))
