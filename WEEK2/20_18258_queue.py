import sys

debugFlag = False

n = list(map(int, sys.stdin.readline().split()))[0]

front    = 0
rear     = 0
capacity = 0
no       = 0
que      = [None] * n

for _ in range(n):
    input_str = list(map(str, sys.stdin.readline().split()))
    cmd = input_str[0]

    if cmd == 'push':
        que[rear] = input_str[1]
        rear += 1
        no   += 1

    elif cmd == 'pop':
        if(no == 0):
            print(-1)
        else:
            print(que[front])
            que[front] = None
            front += 1
            no -= 1
    elif cmd == 'size':
        print(no)
    elif cmd == 'empty':
        if(no == 0): print(1)
        else: print(0)
    elif cmd == 'front':
        if(no == 0): print(-1)
        else: print(que[front])
    elif cmd == 'back':
        if(no == 0): print(-1)
        else: print(que[rear-1])
    else:
        pass

    if debugFlag: print(que)
