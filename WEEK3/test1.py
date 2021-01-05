import sys
from collections import deque
input = sys.stdin.readline

dr = [1,0,0,-1]
dc = [0,1,-1,0]

n = int(input())
house_str = list(input() for _ in range(n))
house_map = [[0 for col in range(n)] for row in range(n)]

for i in range(n):
    for j in range(n):
        house_map[i][j] = int(house_str[i][j])



visited = [[0 for col in range(n)] for row in range(n)]
def bfs(root):    

    queue = [root]
    house_cnt = 1                                     # 큐에 시작점을 줄 세움

    while queue:                                           # 큐가 빌떄까지 탐색을 계속
        row, col = queue.pop(0)

        visited[row][col] = 1
        
        for i in range(4):
            rr = row + dr[i]; cc = col + dc[i]
            if 0 <= rr < n and 0 <= cc < n:
                if house_map[rr][cc] == 1 and not visited[rr][cc] and [rr,cc] not in queue:
                    queue.append([rr,cc])
                    house_cnt += 1

    return house_cnt


#처음 시작점 찾기
start =[0,0]
isBreak = 0
for i in range(n):
    for j in range(n):
        if house_map[i][j] == 1: start =[i,j]; isBreak = 1; break
    if isBreak: break


village = 0
answer = []
while True:    
    
    village += 1

    answer.append(bfs(start))

    # 다음 시작점 찾기
    isBreak = 0
    canStart = 0
    for i in range(n):
        for j in range(n):
            if visited[i][j] == 0 and house_map[i][j]: 
                start = [i,j];
                isBreak =1; canStart = 1
                break    
        if isBreak: break    

    if canStart == 0: break # 다음 시작할 점이 없으면 검색 완료





print(village)
answer.sort()
for i in range(len(answer)): print(answer[i])
