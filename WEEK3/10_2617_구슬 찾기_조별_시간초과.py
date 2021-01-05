import sys
from collections import deque

n, m = map(int,sys.stdin.readline().split())

compareNum = (n+1)//2

graphHeavy = [[] for _ in range(n+1)]
graphLight = [[] for _ in range(n+1)]
visitHeavy = [0] * 100 
visitLight = [0] * 100

for _ in range(m):
    heavyBall, lightBall = map(int,sys.stdin.readline().split())
    graphHeavy[heavyBall].append(lightBall) 
    graphLight[lightBall].append(heavyBall)

cntHeavy = 0
cntLight = 0


def dfsHeavy(graph, v):
    global cntHeavy
    visitHeavy[v] = 1
    for i in graph[v]:
        if visitHeavy[i] == 0:
            cntHeavy += 1
            dfsHeavy(graph,i)
            # visitHeavy[i] = 0

def dfsLight(graph, v):
    global cntLight
    # cntLight += 1
    visitLight[v] = 1
    for i in graph[v]:
        if visitLight[i] == 0:
            cntLight += 1
            dfsLight(graph,i)
            # visitLight[i] = 0

ans = 0
for i in range(1, n+1):
    dfsHeavy(graphHeavy,i)
    if compareNum <= cntHeavy:
        ans += 1
    else:
        dfsLight(graphLight,i)
        if compareNum <= cntLight:
            ans += 1

    cntHeavy = 0
    cntLight = 0
    
    visitHeavy = [0]*100
    visitLight = [0]*100

print(ans)