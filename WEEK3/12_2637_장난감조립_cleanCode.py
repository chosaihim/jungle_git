import sys
input = sys.stdin.readline

#### INPUT ####
N = int(input()); M = int(input())

graph = [[] for _ in range(N+1)]
indeg = [ 0 for _ in range(N+1)]


#### 초기변수 세팅 ####
# Graph, indegree
for _ in range(M):
    parent, child, weight = map(int, input().split())
    graph[parent].append([child,weight])
    indeg[child] += 1
for i in range(N+1): graph[i].sort()

# in_weight: 각 노드로 들어오는 weight의 합
in_weight = [0 for _ in range(N+1)]
in_weight[-1] = 1

# zeroIn: 해당 노드에서 나가는 간선이 하나도 없는 것들만 찾아서 저장(기본부품)
zeroIn = []
for i in range(N+1):
    if not graph[i]: zeroIn.append(i)
zeroIn.sort()



#### MAIN ####
queue = []
queue.append(N) # Finished Product is always zero indegree node
while queue:

    node = queue.pop(0)
    node_weight = in_weight[node]
    
    for child in graph[node]:
        node_num, connect_weight = map(int, child)
        
        indeg[node_num] -= 1
        in_weight[child[0]] += connect_weight * node_weight
    
        if indeg[child[0]] == 0:
            queue.append(child[0])
            indeg[child[0]] = -1

#### 정답 출력 ####
zeroIn.pop(0) #젤 처음에 노드가 0인 존재하지 않는 노드가 있어서 제거
for i in zeroIn:
    print(f'{i} {in_weight[i]}')