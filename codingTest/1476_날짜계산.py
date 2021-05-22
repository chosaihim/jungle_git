import sys
input = sys.stdin.readline

E, S, M = map(int,input().split())

#15,28,19
year = 0; e = 0; s = 0; m = 0
while True:
    if e == E and s == S and m == M:
        break
    
    e += 1; s+= 1; m+= 1
    
    if e > 15: e = 1
    if s > 28: s = 1
    if m > 19: m = 1
    
    year += 1

print(year)

# 나머지로 풀기
#15,28,19
year = 0; e = 0; s = 0; m = 0
while True:
    
    e = (year)%15
    s = (year)%28
    m = (year)%19
    
    if E-1 == e and S-1 == s and M-1 == m:
        break
    
    year += 1

print(year+1)