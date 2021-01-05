import sys

n      = list(map(int, sys.stdin.readline().split()))[0]
towers = list(map(int, sys.stdin.readline().split()))

stk = [None]*n
ptr = 0
result = [0]*n

for i in range(len(towers)):
    
    tower = towers[i]

    while True:
        if ptr == 0:
            stk[ptr] = i+1
            ptr += 1
            break
        elif towers[stk[ptr-1]-1] > tower:            
            result[i] = stk[ptr-1]
            stk[ptr] = i+1
            ptr += 1
            break
        else:
            ptr -= 1
            stk[ptr] = None

for res in result:
    print(res,end=' ')