import sys
from collections import deque
input = sys.stdin.readline

com  = int(input())
pair = int(input())

graph = [[] for _ in range(com+1)]
for _ in range(pair):
    i, j = map(int, input().split())
    graph[i].append(j)
    graph[j].append(i)

def bfs(graph, root):
    visited = []    # 방문한 곳을 기록
    queue = [root]  # 큐에 시작점을 줄 세움

    while queue:    # 큐가 빌떄까지 탐색을 계속
        vertex = queue.pop(0)

        if vertex not in visited: # 꼭지점에 방문한 적 없다면 방문 기록에 추가
            visited.append(vertex)
            for node in graph[vertex]:  # 꼭지점에 연결된 노드들 중에서 
                if node not in visited: # 방문 안 된 곳만을
                    queue.append(node)
    return visited

print(len(bfs(graph,1))-1)


