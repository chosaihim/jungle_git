import sys
# debugFlag = True
debugFlag = False

# Main
n = list(map(int, sys.stdin.readline().split()))[0]

stk =[None]*n
ptr = 0
for _ in range(n):
    stick = list(map(int, sys.stdin.readline().split()))[0]
    
    while True:
        if ptr == 0: 
            stk[ptr] = stick
            ptr += 1
            if debugFlag: stk[ptr] = -1
            break
        elif(stk[ptr-1] > stick):
            stk[ptr] = stick
            ptr += 1
            if debugFlag: stk[ptr] = -1
            break
        elif(stk[ptr-1] <= stick):
            stk[ptr] = None
            ptr -= 1
            if debugFlag: stk[ptr] = -1

print(ptr)