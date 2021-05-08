import sys
sys.setrecursionlimit(10**7)

def solution(n, path, order):
    answer = False
    graph= [[] for _ in range(n)]

    for p in path:
        graph[p[0]].append(p[1])
        graph[p[1]].append(p[0])
    
    order_dic = {}
    for o in order:
        order_dic[o[1]] = o[0]
    # print(order_dic)
    
    visited = [0] * n
    count = [0]

    def dfs(room):
        # print(f"in {room}")
        visited[room] = 1
        count[0] += 1
        
        for r in graph[room]:
            # print("r:",r)
            if order_dic.get(r) and visited[order_dic[r]] and visited[r]==0:
                dfs(r)
            elif visited[r] == 0:
                dfs(r)
        
        # print(f"out {room}")
    
    # print(graph)
    # print(dfs(0))
    dfs(0)
    # print(count[0])
    
    if count[0] == n: answer = True
    
    return answer





n = 9
path = [[0,1],[0,3],[0,7],[8,1],[3,6],[1,2],[4,7],[7,5]]
order =  [[8,5],[6,7],[4,1]]
print(solution(n,path,order))