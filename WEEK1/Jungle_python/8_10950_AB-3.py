import sys  
n = list(map(int, sys.stdin.readline().split()))[0]

sum = []

for i in range(n):
    a,b= list(map(int, sys.stdin.readline().split()))
    sum.append(a+b)

    

for i in range(n):
    print(sum[i])
    