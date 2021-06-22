import sys
from itertools import combinations
input = sys.stdin.readline

n, m = map(int, input().split())
l = list(map(int,input().split()))
l.sort()

for combination in list(combinations(l,m)):
    for c in combination:
        print(c, end = ' ')
    print()