import sys
input = sys.stdin.readline

N, M = map(int, input().split())
graph = [[] for _ in range(N+1)]

for _ in range(M):
    parent, child = map(int, input().split())
    graph[parent].append(child)




answer = []
visited = []

def dfs(start):    
    visited.append(start)

    if not graph[start]:
        if start not in answer: 
            answer.append(start)
        return None
    
    dfsCall = 0
    for node in graph[start]:
        if node not in visited and node not in answer:
            dfs(node)
            visited.pop()
            dfsCall += 1
        else: graph[start].remove(node)

i = 1
while len(answer) < N:
    if i not in visited:
        dfs(i)
        visited.pop()
    i += 1
    if(i>N): i=1

for node in reversed(answer):
    print(node,end=' ')