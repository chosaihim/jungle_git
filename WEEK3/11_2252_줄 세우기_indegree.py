import sys
input = sys.stdin.readline

##### INPUT #####
N, M = map(int, input().split())
graph = [[] for _ in range(N+1)]
indegree = [0 for _ in range(N+1)]


for _ in range(M):
    parent, child = map(int, input().split())
    graph[parent].append(child)
    indegree[child] += 1

### END INPUT

queue = []
answer = []

for node in range(1,len(indegree)):
    if indegree[node] == 0:
        queue.append(node)

while queue:
    for _ in range(len(queue)):
        root = queue.pop(0)
        answer.append(root)
        for child in graph[root]:
            indegree[child] -= 1
            if indegree[child] == 0:
                queue.append(child)
    
for ans in answer: print(ans,end=' ')