import sys
import heapq
debugFlag = True
# debugFlag = False

k, n = list(map(int, sys.stdin.readline().split()))
sosu = list(map(int, sys.stdin.readline().split()))

hque = []   # heap que
maxh = []   # max heap
heapq.heapify(maxh)
for so in sosu: heapq.heappush(hque,so)

answer = 0
cnt = 0
while cnt < n:
    answer = heapq.heappop(hque)

    heapq.heappush(hque,answer*answer)
    for i in range(len(hque)):
        heapq.heappush(hque,hque[i]*answer)
        heapq.heappush(maxh,-hque[i]*answer)
    
    cnt += 1

print(answer)
