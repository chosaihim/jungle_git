import sys
input = sys.stdin.readline

#### INPUT ####
N = int(input()); M = int(input())

graph = [[] for _ in range(N+1)]
indeg = [ 0 for _ in range(N+1)]
total_weight = [0 for _ in range(N+1)]
total_weight[-1] = 1


for _ in range(M):
    parent, child, weight = map(int, input().split())
    graph[parent].append([child,weight])
    indeg[child] += 1

zeroIn = []
for i in range(N+1):
    if not graph[i]: zeroIn.append(i)
zeroIn.sort()

for i in range(N+1): graph[i].sort()


queue = []

# Finished Product is always zero indegree node
queue.append(N)

while queue:
    for _ in range(len(queue)):
        node = queue.pop(0)
        node_weight = total_weight[node]
        
        for child in graph[node]:
            node_num, weight = map(int, child)
            
            indeg[node_num] -= 1
            total_weight[child[0]] += weight * node_weight
            if indeg[child[0]] == 0:
                queue.append(child[0])
                indeg[child[0]] = -1
        
zeroIn.pop(0)
for i in zeroIn:
    print(f'{i} {total_weight[i]}')