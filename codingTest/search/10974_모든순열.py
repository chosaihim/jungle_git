import sys
from itertools import permutations
input = sys.stdin.readline

n = int(input())

l = [i for i in range(1, n+1)]

for one in list(permutations(l,n)):
    for i in list(one):
        print(i, end= ' ')
    print()
    

#76ms
# from itertools import permutations
# import sys
# print=sys.stdout.write
# def BOJ10974():
#     n = int(input())
#     for i in map(" ".join,permutations([str(i) for i in range(1,n+1)])):
#         print(i+"\n")
# BOJ10974()