import sys
input = sys.stdin.readline

N = int(input())
devider = 2

while N > 1:
    # print(N)
    if N % devider == 0:
        print(devider)
        N = N // devider
    else:
        devider += 1

    