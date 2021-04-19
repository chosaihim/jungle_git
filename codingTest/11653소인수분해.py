import sys
input = sys.stdin.readline

N = int(input())
sq=round(N**(1/2))+1
divider = 2

while N > 1:
    if N % divider == 0:
        print(divider)
        N = N // divider
    else:
        divider += 1
        if divider > sq :
            print(N)
            break

    