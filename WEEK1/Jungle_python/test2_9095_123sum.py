import sys  
T = list(map(int, sys.stdin.readline().split()))[0]
cnt = 0


def adding(original, current):
    global cnt

    if(current > original):
        return None
    elif(current == original):
        cnt += 1
        return None
    else:
        adding(original,current+1)
        adding(original,current+2)
        adding(original,current+3)

    return None

for i in range(T):
    n = list(map(int, sys.stdin.readline().split()))[0]
    cnt = 0
    adding(n,0)
    print(cnt)
