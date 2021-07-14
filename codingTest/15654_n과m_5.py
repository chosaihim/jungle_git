import sys
from itertools import permutations
input = sys.stdin.readline

n, m = map(int, input().split())
l = list(map(int,input().split()))
l.sort()

for permutation in list(permutations(l,m)):
    for p in permutation:
        print(p, end = ' ')
    print()

