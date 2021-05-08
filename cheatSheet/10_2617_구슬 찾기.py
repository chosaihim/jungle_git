import sys
from collections import deque
input = sys.stdin.readline


##### INPUT #####
N, M = map(int, input().split())    # n: num of bead, m: num of pairs
min_tree = [[] for _ in range(N+1)]
max_tree = [[] for _ in range(N+1)]


for _ in range(M):
    big, small = map(int, input().split())
    max_tree[0].append(big)
    max_tree[big].append(small)
    
    min_tree[0].append(big)
    min_tree[small].append(big)

print(min_tree)
print(max_tree)

visited = [0 for _ in range(N+1)]

### DFS
def dfs(node):
    visited[node] = 1
    print(node, end='-')
    for child in graph[node]:
        # if visited[child] == 0:/
        dfs(child)
        print()

dfs(0)


