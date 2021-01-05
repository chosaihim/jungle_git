import sys

braskets = list(map(str, sys.stdin.readline().split()))[0]

# print(f'braskets:{braskets}, len:{len(braskets)}')

trueFlag = True
ptr = 0
stk = []
answer = 1
# total = 1
# total_sum = 0
# total = 1
total = 0

for brasket in braskets:
    # print(f'brasket:{brasket}')

    while True:
        
        # print(f'total:{total}')
        # print(f'len(stk):{len(stk)}')

        if brasket == "(" :
            stk.append(brasket)
            break
        
        elif brasket == "[":
            stk.append(brasket)
            break

        elif brasket == ")":
            if len(stk) == 0 : trueFlag = False; break
            top = stk.pop()
            if top == "(":
                if total == 0: total=1                
                stk.append(total*2)
                total = 0
                # total *= 2
                # stk.append(total)
                # total = 1
                break
            elif type(top) == int : total += top
            else: trueFlag = False; answer = 0; break
        
        else:
            if len(stk) == 0 : trueFlag = False; break
            top = stk.pop()
            if top == "[":
                if total == 0: total=1                
                stk.append(total*3)
                total = 0
                break
            elif type(top) == int : total += top
            else: trueFlag = False; answer = 0; break
        
    
    # print(f'stack: {stk}')
    if not trueFlag: break

# if trueFlag: print(0)
# else: print(keep)
# print(answer)

if not trueFlag: print(0)
else:
    if not type(stk[0])== int: print(0)
    else: print(sum(stk))