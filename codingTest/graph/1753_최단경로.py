import sys
input = sys.stdin.readline
import heapq

# 전체 노드의 개수와 간선의 개수
V, E = map(int, input().split()) 
# 시작 노드
start = int(input())
# 무한대값 설정
INF = 1000000000
# 노드들의 연결 정보 리스트
graph = [[] for _ in range(V+1)]
# start로부터 각 노드까지의 최단거리. INF로 초기화
distance = [INF] * (V+1)

# 노드들의 연결 정보 받아오기
for _ in range(E):
    u, v, w = map(int, input().split())
    # u라는 노드부터 v라는 노드까지의 거리가 w
    graph[u].append([v,w])



def dijkstra(start):
    # 시작 노드으로부터 시작 노드까지의 거리는 0
    distance[start] = 0
    heap = []
    # 시작 노드로부터 시작 노드까지의 최소거리는 0이므로 (최소거리, 도착노드)를 넣어줌
    heapq.heappush(heap, (0, start))
    
    while heap:
        # 현재 노드와 현재 노드로 도달하기까지의 거리
        dist, node = heapq.heappop(heap)
        
        # distance table의 시작점에서 현재 노드까지의 거리가 현재 거리보다 작으면 넘어감
        if distance[node] < dist: continue
        # 현재 거리가 테이블의 거리보다 짧으면 현재 노드에서 갈 수 있는 모든 노드 검사
        for connected_node in graph[node]:
            # 다음 노드와 다음 노드로 건너가기 위한 거리
            next_node, d = map(int, connected_node)
            # 시작점에서 다음 노드까지의 거리는 현재 거리 + 현재 노드에서 다음 노드까지의 거리
            next_dist = d + dist
            # next_dist가 distance 리스트에 저장된 것보다 작으면
            if next_dist < distance[next_node]:
                # 리스트 업데이트
                distance[next_node] = next_dist
                # 힙에 넣어줌
                heapq.heappush(heap,(next_dist, next_node))
    

# 정해진 시작점으로부터 각 노드까지의 최단 거리 구하기
dijkstra(start)

# 최단 거리가 INF 보다 작으면 최단거리 출력 아니면 "INF" 출력
for i in range(1, V+1):
    print(distance[i] if distance[i] < INF else "INF")
    

# ## 624ms
# import sys
# from heapq import *

# def dykstra(graph, start, distance):
#     q = []
#     heappush(q, (0, start))
#     distance[start] = 0
#     while q:
#         dist, node = heappop(q)
#         if distance[node] < dist:
#             continue
#         for i in graph[node]:
#             cost = dist + i[1]
#             if cost < distance[i[0]]:
#                 distance[i[0]] = cost
#                 heappush(q, (cost, i[0]))

# def solution():
#     input = sys.stdin.readline
#     INF = float("inf")

#     v, e = map(int, input().split())
#     start = int(input())
#     graph = [[] for _ in range(v+1)]
#     distance = [INF] * (v+1)

#     for _ in range(e):
#         a, b, c = map(int, input().split())
#         graph[a].append((b, c))
                    
#     dykstra(graph, start, distance)

#     for i in range(1, v+1):
#         if distance[i] == INF:
#             print("INF")
#         else:
#             print(distance[i])

# solution()