import sys
from collections import deque
read=sys.stdin.readline

def melt(save_point):
    melt_cnt = 0
    checked_cnt = 1
    nonzero_point = [-1,-1]
    point = deque([save_point])
    visited = list(list(1 for _ in range(m)) for _ in range(n))
    visited[save_point[0]][save_point[1]] = 0
    while point:
        a,b = point.popleft()
        #print(a,b)
        for x,y in zip(dx,dy):
            ax, by = a+x, b+y
            if 0<=ax<n and 0<=by<m and visited[ax][by] and ocean[ax][by]:
                point.append([ax,by])
                visited[ax][by] = 0
                checked_cnt += 1
        for x,y in zip(dx,dy):
            ax, by = a+x, b+y
            if 0<=ax<n and 0<=by<m and not ocean[ax][by] and visited[ax][by]:
                if ocean[a][b] > 1:
                    ocean[a][b] -= 1
                else:
                    ocean[a][b] = 0
                    melt_cnt += 1
                    break
        if ocean[a][b]:
            nonzero_point = [a,b]
    return melt_cnt, checked_cnt, nonzero_point


dx = [1,0,0,-1]
dy = [0,1,-1,0]

n,m = map(int,read().split())
ocean = list(list(map(int,read().split())) for _ in range(n))
total_cnt = 0

for i in range(n):
    for j in range(m):
        if ocean[i][j] != 0:
            total_cnt += 1
            save_point = (i,j)


if total_cnt == 0:
    print(0)
    exit()
time = 0
while True:
    melt_cnt, checked_cnt, nonzero_point = melt(save_point)
    save_point = nonzero_point
    #print(nonzero_point)
    #for o in ocean:
    #    print(*o)
    #print()
    if total_cnt != checked_cnt:
        print(time)
        break
    total_cnt -= melt_cnt
    if total_cnt == 0:
        print(0)
        break
    time += 1