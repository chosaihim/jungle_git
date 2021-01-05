import sys

n = list(map(int, sys.stdin.readline().split()))[0]
towers = list(map(int, sys.stdin.readline().split()))

ptr = 0
front = 1
recieved =[0]*n
stk = [None]*n

for i in range(len(towers)):
    tower = towers[i]
    l_flag = False

    # print(f'**** i:{i}, tower:{tower}')

    while True:
        # print(f'ptr:{ptr}')    
        if(ptr == 0):
            
            # print(">>> 0")
            front = i + 1
            stk[ptr] = tower
            ptr += 1
            # print(f'recieve:{recieved}')
            # print(stk)
            break
        elif stk[ptr-1] > tower:
            # print(">>> 1")
            if(l_flag): recieved[i] = front
            else: recieved[i] = i
            # print(f'recieve:{recieved}')

            stk[ptr] = tower
            ptr += 1
            
            # print(stk)
            break            
        else:
            l_flag = True
            ptr -= 1
            stk[ptr]=None
            
            # print(stk)

for recieve in recieved:
    print(recieve, end=' ')
        
