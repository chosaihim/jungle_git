import sys
# debugFlag = True
debugFlag = False

n, k = list(map(int, sys.stdin.readline().split()))

original = input()
l_origin =[0]*n
for i in range(n): l_origin[i] = int(original[i])

if debugFlag: print(f'l_origin: {l_origin}')

skipped  = 0
skipfull = False

stk_len = n - k
stk = []
for i in range(n):

    if(stk_len == 0): break
    while True:
        # if(input() == 'q'): break      

        if(len(stk)==0):
            stk.append(l_origin[i])
            break
        
        if debugFlag: print(f'stk[-1]:{stk[-1]}, origin[{i}]:{l_origin[i]}')

        if(stk[-1] < l_origin[i] and skipped < k):
            stk.pop()
            skipped += 1
        elif(len(stk) < stk_len):
            stk.append(l_origin[i])
            break
        else:
            break
    
    # print(stk)

for digit in stk:
    print(digit,end='')

