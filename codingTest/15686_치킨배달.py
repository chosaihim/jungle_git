import sys
from itertools import combinations
input = sys.stdin.readline

n, m = map(int, input().split())
village = [list(map(int, input().split())) for _ in range(n)]

houses = []
chickens = []
for row in range(n):
    for col in range(n):
        if village[row][col] == 1: houses.append([row,col])
        elif village[row][col] == 2: chickens.append([row,col])


def find_dist(house, chicken):
    return abs(house[0]-chicken[0])+abs(house[1]-chicken[1])

chickens = list(combinations(chickens,m))

dist = []
min_sum_dist = 99999999999
for chicken in chickens:
    for house in houses:
        min_dist = 99999999999
        for store in chicken:
            min_dist = min(min_dist, find_dist(house,store))
        dist.append(min_dist)
        
    min_sum_dist = min(min_sum_dist, sum(dist))
    dist.clear()

print(min_sum_dist)

#112ms 코드 비교해 보기!
# from sys import stdin
# from itertools import combinations as comb
# r = stdin.readline

# n,m = map(int, r().strip().split())
# city = [r().strip().split() for i in range(n)]
# ans = 1e9
# houses = []
# chickens = []
# for i in range(n):
#     for j in range(n):
#         if city[i][j] == '1':
#             houses.append((i,j))
#         elif city[i][j] == '2':
#             chickens.append((i,j))

# dists = [list(map(lambda x : abs(x[0]-c[0]) + abs(x[1]-c[1]), houses)) for c in chickens]
# for co in comb((i for i in range(len(chickens))), m):
#     res = sum(map(min, zip(*[dists[i] for i in co])))


#     if res < ans:
#         ans = res
# print(ans)
    
    


    