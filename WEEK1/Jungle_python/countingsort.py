import sys
input = sys.stdin.readline
n = int(input())
a = [0] * 10001
maxx = 0
tmp = 0 
for i in range(n):
    tmp = int(input())
    a[tmp]+=1
    maxx = max(maxx, tmp)
for j in range(10000+1):
    for i in range(a[j]):
        print(j)
        
import sys
n = int(sys.stdin.readline())
cnt = [0 for i in range(10000+1)]
for i in range(n):
    cnt[int(sys.stdin.readline())] += 1
for i in range(1, 10000+1):
    for j in range(cnt[i]):
        print(i)