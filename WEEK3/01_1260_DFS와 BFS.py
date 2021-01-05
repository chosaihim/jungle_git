import sys
from collections import deque
input = sys.stdin.readline

N, M, V = map(int, input().split())
graph = [[] for _ in range(N+1)]

# 리스트를 이용한 인접 리스트 구현
for _ in range(M):
    i, j = map(int, input().split())
    graph[i].append(j)
    graph[j].append(i)


for i in range(N):
    graph[i].sort()



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

def dfs(graph, root):
    visited = []
    stack = [root]

    while stack:
        vertex = stack.pop()
        
        if vertex not in visited:
            visited.append(vertex)
            for node in reversed(graph[vertex]):
                if node not in visited:
                    stack.append(node)

    return visited

print(" ".join(map(str, dfs(graph,V))))
print(" ".join(map(str, bfs(graph,V))))