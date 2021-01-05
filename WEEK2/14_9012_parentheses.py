import sys
# debugFlag = True
debugFlag = False

def isAppropriate(prnths):
    ptr = 0
    length = len(prnths)

    for prnth in prnths:
        if(prnth == "(" ): 
            ptr += 1
            if ptr > len(prnths): return False
        else:
            ptr -= 1
            if ptr < 0: return False

    if(ptr == 0): return True
    else: return False

# Main
t = list(map(int, sys.stdin.readline().split()))[0]


for _ in range(t):
    prnths = list(map(str, sys.stdin.readline().split()))[0]

    if(isAppropriate(prnths)): print("YES")
    else: print("NO")

    