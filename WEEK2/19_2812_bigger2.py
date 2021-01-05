import sys
# debugFlag = True
debugFlag = False

n, k = list(map(int, sys.stdin.readline().split()))

original = list(map(str, sys.stdin.readline().split()))[0]
l_origin =[0]*n
for i in range(n): l_origin[i] = int(original[i])

if debugFlag: print(f'l_origin: {l_origin}')

skipped  = 0
skipfull = False

stk_len = n - k
stk = [None] * stk_len
ptr = 0
for i in range(n):
    
    while True:
        
        if(ptr == 0):
            stk[ptr] = l_origin[i]
            ptr += 1
            break

        if(stk[ptr-1] < l_origin[i] and skipped < k):
            # stk.pop()
            ptr -= 1
            stk[ptr] = None
            skipped += 1
        elif(ptr < stk_len):
            # stk.append(l_origin[i])
            stk[ptr] = l_origin[i]
            ptr += 1
            break

    # print(stk)

for i in range(len(stk)):
    print(stk[i],end='')

