import sys
from collections import deque
input = sys.stdin.readline
sys.setrecursionlimit(10**9)

N, K = map(int, input().split())

visited = [0 for i in range(100001)]
### END INPUT


min_depth = 100001
def dfs(node, depth):
    global min_depth

    # print(f'node:{node} current depth:{depth}, min depth:{min_depth}')

    # print(f'node:{node}')
    visited[node] = 1

    if node == K:  min_depth = min(min_depth, depth); #print(f'mindepth:{min_depth}')
    else:
        if depth < min_depth:

            dd = [-1, 1 , node]

            for d in dd:
                new = node + d            
                
                if 0 <= new <= 100000 and visited[new] == 0:
                    dfs(new, depth+1)
                    visited[new] = 0


dfs(N,0)
print(min_depth)

