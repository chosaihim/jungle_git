import sys
import heapq
# debugFlag = True
debugFlag = False

n = list(map(int, sys.stdin.readline().split()))[0]


que = []
for _ in range(n):
    # cards.append(list(map(int, sys.stdin.readline().split()))[0])
    new = list(map(int, sys.stdin.readline().split()))[0]
    
    heapq.heappush(que, new)

if debugFlag: print(f'heapq:{que}')

answer = 0
if n == 1: answer = 0
else:
    while True:

        
        if(len(que) == 1):
            break
        
        answer1 = heapq.heappop(que)
        answer2 = heapq.heappop(que)

        t_answer = answer1 + answer2
        heapq.heappush(que,t_answer)

        answer += t_answer



print(answer)
