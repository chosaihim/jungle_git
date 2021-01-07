import sys
input = sys.stdin.readline

n = int(input())

d = [0] * (n+1)
def dp(x):
    if x == 1: return 1
    if x == 2: return 3
    if(d[x] != 0): return d[x]
    
    d[x] = (2*dp(x-2) + dp(x-1))%10007
    return d[x]

print(dp(n))

