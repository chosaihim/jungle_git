import sys
input = sys.stdin.readline


k, n = map(int, input().split())
wires = [int(input()) for _ in range(k)]


def bin_search(goal, wires):
    pl = 1
    pr = max(wires)
    max_length = 0
    
    while True:
        pc = (pl + pr) //2
        
        count = 0
        for wire in wires:
            count += wire//pc
        
        if count < goal:
            pr = pc - 1
        else:
            max_length = max(max_length, pc)
            pl = pc + 1
            
        if pl > pr:
            break
        
    return max_length

print(bin_search(n, wires))
            
            
        