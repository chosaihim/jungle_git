import sys
input = sys.stdin.readline

N, M = map(int, input().split())
graph = [[] for _ in range(N+1)]
indegree = [0 for _ in range(N+1)]
total_in = 0

indeg = [None for _ in range(N+1)]


for _ in range(M):
    parent, child = map(int, input().split())
    graph[parent].append(child)
    indegree[child] += 1
    total_in += 1

# print(graph)
# print("indegree:", indegree)

queue = []
answer = []

while total_in >= 0:

    for i in range(1,N+1):
        if not indegree[i] and i not in answer:
            queue.append(i)
    
    # print(queue)
    
    for _ in range(len(queue)):
        root = queue.pop(0)
        # print(queue)
        answer.append(root)
        total_in -= 1

        for node in graph[root]:
            indegree[node] -= 1
    
    # print("answer:", answer)
        
# print(answer)
for ans in answer: print(ans,end=' ')


# print(" ".join(map(int, answer)))