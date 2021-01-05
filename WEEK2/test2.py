import sys
input = sys.stdin.readline

laser = input()

stk = []
total = 0

for i in range(len(laser)-1):
    
    if i == 0: stk.append(laser[0]); continue   
    
    if laser[i] == "(" : stk.append(laser[i])
    else:
        stk.pop()
        if laser[i-1] == "(" : total += len(stk)
        else: total += 1
    
    # print(stk)

print(total)