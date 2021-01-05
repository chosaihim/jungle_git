import sys
from collections import deque
input = sys.stdin.readline
sys.setrecursionlimit(10**9)

### INPUT
n = int(input())
graph = [[] for _ in range(n+1)]
for _ in range(n-1):
    n1, n2 = map(int, input().split())
    graph[n1].append(n2)
    graph[n2].append(n1)

visited = [0 for _ in range(n+1)]
### END INPUT

def dfs(node):
    visited[node] = 1

    for child in graph[node]:
        if visited[child] == 0:
            # print(f'-{child}', end='-')
            answer[child] = node
            dfs(child)
   
answer = [0]*(n+1)     
dfs(1)
for i in range(2,n+1): print(answer[i])