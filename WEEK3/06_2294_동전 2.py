import sys
from collections import deque
input = sys.stdin.readline

##### INPUT #####
n, k = map(int, input().split())  # n: num of coins, k: goal
coins = []
for _ in range(n):
    coin = int(input())
    if coin not in coins: coins.append(coin)
### END INPUT ###


### GRAPH
coins.sort()
graph={}
graph[0] = []
for i in range(len(coins)):
    if coins[i] > k: break
    graph[0].append(coins[i])
    graph[coins[i]] = []
    for j in range(i,len(coins)):
        graph[coins[i]].append(coins[j])


#최대 loop 수:
loop_max = k//coins[0] + 1 

### BFS
def bfs(root):
    queue = deque([root])  # 큐에 시작점을 줄 세움
    depth = 0
    
    totals = [False]*10001 # 시간 초과 때문에 뒤에 계속 붙이는 형태로 쓰지 않고 물리적으로 개수 선언함

    while queue and depth < loop_max:    # 큐가 빌떄까지 탐색을 계속
        vertex = queue.popleft()
        total = vertex[0] + vertex[1]
        depth = vertex[2]
        # print(f'vertex: {vertex}, total:{total}')

        if total > k: continue
        elif total == k: return depth
        
        # if total not in totals:
            # totals.append(total)
        # else: continue
        if totals[total]: continue
        else: totals[total] = True

        for node in graph[vertex[0]]:  # 꼭지점에 연결된 노드들 중에서 
            queue.append([node,total,depth+1])
            # print(f'node:{node}')
    
    return -1

print(bfs([0,0,0]))
