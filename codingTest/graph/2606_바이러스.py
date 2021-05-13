import sys
input = sys.stdin.readline

#### INPUT ####
num_computers = int(input()); num_pairs = int(input())
graph = [[] for _ in range(num_computers+1)]
for _ in range(num_pairs):
    i, j = map(int, input().split())
    graph[i].append(j)
    graph[j].append(i)

def bfs(graph,root):
    visited = []
    queue = [root]
    
    while queue:
        vertex = queue.pop(0)
        
        if vertex not in visited:
            visited.append(vertex)
            
            for node in graph[vertex]:
                if node not in visited:
                    queue.append(node)
    
    return visited

print(len(bfs(graph,1))-1)