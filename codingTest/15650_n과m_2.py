import sys
from itertools import combinations
input = sys.stdin.readline

n, m = map(int, input().split())
l = [i for i in range(1,n+1)]

for combination in list(combinations(l,m)):
    for c in combination:
        print(c, end = ' ')
    print()