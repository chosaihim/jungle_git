import sys

k = list(map(int, sys.stdin.readline().split()))[0]

stk = [0]*k
ptr = 0
for _ in range(k):
    k_input = list(map(int, sys.stdin.readline().split()))[0]

    if(k_input==0):
        ptr -= 1
        stk[ptr] = 0
    else:
        stk[ptr] = k_input
        ptr += 1

    # print(stk)
print(sum(stk))