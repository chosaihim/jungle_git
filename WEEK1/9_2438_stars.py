import sys  
n = list(map(int, sys.stdin.readline().split()))[0]

for i in range(n):
    for j in range(i+1):
        print("*",end='')
    print()