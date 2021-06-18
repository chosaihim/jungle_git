import sys
input = sys.stdin.readline

n = int(input())
graph = []
other_color = [[1,2],[0,2],[0,1]]

def dfs(index, color):
    cost = 0
    min_cost = 1000001
    
    if index == n-1:
        return graph[index][color]
    
    for next_color in other_color[color]:
        curr_cost = graph[index][color]
        next_cost = dfs(index+1, next_color)
        cost = curr_cost + next_cost
        min_cost = min(min_cost, cost)

    
    return min_cost
    

for i in range(n):
    r,g,b = map(int,input().split())
    graph.append([r,g,b])
    
print(graph)
    
min_cost = 1000001
for color in range(3):
    min_cost = min(min_cost, dfs(0,0))

print(min_cost)
    

# 3
# 26 40 83
# 49 60 57
# 13 89 99

# 2
# 1 2 3
# 4 5 6