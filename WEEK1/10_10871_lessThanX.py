import sys  
n, x= list(map(int, sys.stdin.readline().split()))

arr = list(map(int, sys.stdin.readline().split()))

for i in range(n):
    if(arr[i] < x):
        print(arr[i],end=' ')