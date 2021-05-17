def solution(n, computers):
    answer = 0
    
    visited = [False] * (n)
    
    def bfs(root):
        visited[root] = True
        queue = [root]
        
        while queue:
            node = queue.pop(0)
            
            for computer in range(n):
                if computers[node][computer] and not visited[computer]:
                    visited[computer] = True
                    queue.append(computer)
    
    for node in range(n):
        if not visited[node]:
            answer += 1
            bfs(node)
    
    return answer

n = 3	
computers = [[1, 1, 0], [1, 1, 1], [0, 1, 1]]
# result = 2
print(solution(n, computers))