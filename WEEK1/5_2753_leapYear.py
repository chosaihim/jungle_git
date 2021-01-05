import sys  
a = list(map(int, sys.stdin.readline().split()))
year = a[0]

if (not year%4 and (year%100 or not year%400)):
    print(1)
else:
    print(0)