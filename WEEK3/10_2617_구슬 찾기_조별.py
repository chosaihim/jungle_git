import sys
from collections import deque


n, m = map(int,sys.stdin.readline().split())

compareNum = (n+1)//2

graphHeavy = [[] for _ in range(n+1)]
graphLight = [[] for _ in range(n+1)]
visit = [0] * 100

for _ in range(m):
    heavyBall, lightBall = map(int,sys.stdin.readline().split())
    graphHeavy[heavyBall].append(lightBall) 
    graphLight[lightBall].append(heavyBall)

cntHeavy = 0
cntLight = 0

def dfsHeavy(graph, v):
    global cntHeavy
    queueHeavy = deque([v])
    visit[v] = 1
    while queueHeavy:
        v = queueHeavy.pop()
        for i in graph[v]:
            if visit[i] == 0:
                cntHeavy += 1
                queueHeavy.append(i)
                visit[i] = 1

def dfsLight(graph, v):
    global cntLight
    queueLight = deque([v])
    visit[v] = 1
    while queueLight:
        v = queueLight.pop()
        for i in graph[v]:
            if visit[i] == 0:
                cntLight += 1
                queueLight.append(i)
                visit[i] = 1

ans = 0
for i in range(1, n+1):
    dfsHeavy(graphHeavy,i)
    visit = [0] * 100
    dfsLight(graphLight,i)
    visit = [0] * 100
    if compareNum <= cntHeavy:
        ans += 1
    if compareNum <= cntLight:
        ans += 1
    cntHeavy = 0
    cntLight = 0

print(ans)