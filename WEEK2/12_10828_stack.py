import sys

debugFlag = False

n = int(input())
stk = [None]*n
ptr = 0

for _ in range(n):
    input_str = list(map(str, sys.stdin.readline().split()))
    cmd = input_str[0]

    if cmd == 'push':
        stk[ptr] = input_str[1]
        ptr += 1
    elif cmd == 'pop':
        if(ptr == 0):
            print(-1)
        else:
            print(stk[ptr-1])
            stk[ptr-1] = None
            ptr -= 1
    elif cmd == 'size':
        print(ptr)
    elif cmd == 'empty':
        if(ptr == 0): print(1)
        else: print(0)
    elif cmd == 'top':
        if(ptr == 0): print(-1)
        else: print(stk[ptr-1])
    else:
        pass

    if debugFlag: print(stk)
