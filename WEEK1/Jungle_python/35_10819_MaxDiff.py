import sys
from itertools import combinations, permutations # 조합 라이브러리

n = int((sys.stdin.readline().split())[0])
arr = list(map(int, sys.stdin.readline().split()))

pairs = list(permutations(arr,n))

max_total = 0

for i in range(len(pairs)):
    total = 0
    for j in range(1,len(pairs[i])):
        total += abs(pairs[i][j-1]-pairs[i][j])
    
    if(total > max_total):
        max_total = total

print(max_total)
