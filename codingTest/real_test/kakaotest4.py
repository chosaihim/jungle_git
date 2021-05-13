from collections import deque

def solution(n, start, end, roads, traps):
    answer = 1000000000
    trap = 0
    
    graph = [[[] for node in range(n+1)] for trapped in range(2)]
    visited = [[1000000000 for _ in range(n+1)] for _ in range(2)]
    
    for road in roads:
        print(road)
        #untrapped
        graph[0][road[0]].append([road[1],road[2]])
        #trapped
        graph[1][road[1]].append([road[0],road[2]])
    
    time = 0
    root = [start, time, trap]
    queue = deque([root])
    
    
    while queue:
        node, time, trap = queue.popleft()
        print(node, time, trap)
        visited[trap][node] = time
        
        if node == end:
            answer = min(answer, time)
        
        print(graph[trap][node])
        for next_node in graph[trap][node]:
            if visited[trap][next_node[0]] > time + next_node[1]:
                if next_node[0] in traps: trap = (trap +1) % 2
                queue.append([next_node[0], time + next_node[1], trap])
        
    
    return answer


# n	start	end	roads	traps	result
# 3	1	3	[[1, 2, 2], [3, 2, 3]]	[2]	5
# 4	1	4	[[1, 2, 1], [3, 2, 1], [2, 4, 1]]	[2, 3]	4

n = 4
start = 1
end = 3
roads = [[1, 2, 1], [3, 2, 1], [2, 4, 1]]
traps = [2, 3]
print(solution(n, start, end, roads, traps))