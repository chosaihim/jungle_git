import sys
debugFlag = True
# debugFlag = False

n = list(map(int, sys.stdin.readline().split()))[0]
towers = list(map(int, sys.stdin.readline().split()))

if debugFlag: print(f'n:{n}, towers:{towers}')

ptr = 0
recieved =[0]*n
stk = [None]*n
cnts = [0]*n
front = 1

for i in range(len(towers)):
    tower = towers[i]
    r_flag = False
    if debugFlag: print(f'tower:{tower}')

    while True:
        
        if debugFlag: print(f'front:{front}')
        
        if(ptr == 0):
            stk[ptr] = tower
            ptr += 1

            if debugFlag: print(f'0 stack:{stk}')
            if debugFlag: print(f'recieved:{recieved}')

            break    

        elif stk[ptr-1] > tower:
            if r_flag: break
            recieved[i] = i
            stk[ptr] = tower
            ptr += 1

            if debugFlag: print(f'1 stack:{stk}')
            if debugFlag: print(f'recieved:{recieved}')

            break

        else:
            if(towers[front-1] >= tower):                
                if debugFlag: print(f'front {towers[front-1]} pushed:{front}')
                recieved[i] = front
                r_flag = True
                
            front = i+1
            if debugFlag: print(f'front updated:{front}')

            ptr -= 1
            stk[ptr]=None

            if debugFlag: print(f'2 stack:{stk}')
            if debugFlag: print(f'recieved:{recieved}')

for recieve in recieved:
    print(recieve, end=' ')
        
