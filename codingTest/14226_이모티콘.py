# https://www.acmicpc.net/problem/14226

# 화면에 있는 이모티콘을 모두 복사해서 클립보드에 저장한다.
# 클립보드에 있는 모든 이모티콘을 화면에 붙여넣기 한다.
# 화면에 있는 이모티콘 중 하나를 삭제한다.

import sys
input = sys.stdin.readline
from collections import deque
visited = [[0 for i in range(10000)] for i in range(10000)]

def bfs(goal):
    curr = 1
    root = [1,0,0]
    queue = deque([root])
    visited[1][0] = 1
    
    while queue:
        screen, time, board = queue.popleft()

        if screen == goal: return time
        
        # 하나 삭제
        if not visited[screen-1][board]:
            queue.append([screen-1,time+1,board])
            visited[screen-1][board] = 1
        # 스크린 to 클립보드
        if not visited[screen][screen]:
            queue.append([screen,time+1,screen])
            visited[screen][screen] = 1
        # 클립보드 to 스크린
        if not visited[screen+board][board]:
            queue.append([screen+board,time+1,board])
            visited[screen+board][board] = 1
        
        

n = int(input())
print(bfs(n))


# 내껀 5000ms 이건 60ms
INF = 999999999999999999
s = int(input())
num = [i for i in range(1005)]
i=1
while i<=s:
    j=2
    num[i-1]=min(num[i-1], num[i]+1)
    while i*j<1002:
        num[i*j] = min(num[i*j], num[i]+j)
        num[i*j-1] = min(num[i*j-1], num[i*j]+1)
        j+=1
    i+=1

print(num[s])
 