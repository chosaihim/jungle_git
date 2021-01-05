import sys  
n = list(map(int, sys.stdin.readline().split()))[0]

for i in range(1,10):
    print(n,"*",i, "=", n*i)