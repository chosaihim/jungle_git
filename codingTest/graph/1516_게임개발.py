import sys
input = sys.stdin.readline
from collections import deque

n = int(input())

time = {}
graph = [[] for _ in range(n+1)]
indeg = [0 for _ in range(n+1)]

for node in range(n):
    building = list(map(int, input().split()))
    
    time[node+1] = building[0]
    
    for parent in range(1,len(building)-1):
        graph[building[parent]].append(node+1)
        indeg[node+1] += 1

zero_deg = deque([])
answer   = {}

for node in range(1, n+1):
    if indeg[node] == 0:
        zero_deg.append([node, 0])

while zero_deg:
    node, total = zero_deg.popleft()
    total += time[node]
    
    answer[node] = total
    
    for child in graph[node]:
        indeg[child] -= 1
        if answer.get(child) == None:
            answer[child] = answer[node]
        else:
            answer[child] = max(answer[child], answer[node])
            
        if indeg[child] == 0:
            zero_deg.append([child,answer[child]])

for i in range(1,n+1):
    print(answer[i])

# 4
# 20 -1
# 10 -1
# 1 1 2 -1
# 1000 1 2 3 -1

# wrong
# 20
# 10
# 21
# 1020

# correct
# 20
# 10
# 21
# 1021

#76ms
# import sys
# sys.setrecursionlimit(100000)
# read = sys.stdin.readline
# f = lambda: [*map(int, read().split())]

# n = int(read())
# time = []
# node = [[] for _ in range(n)]
# final = [-1 for _ in range(n)]

# def back(x):
#     tmp = node[x]
#     if final[x] != -1:
#         return final[x]

#     v = 0
#     for i in tmp:
#         t = back(i-1)
#         if v<t:
#             v = t
#     final[x] = v + time[x]
#     return final[x]

# for m in range(n):
#     s = f()
#     time.append(s[0])
#     node[m] += s[1:-1]

# for i in range(n):
#     back(i)
#     print(final[i])
