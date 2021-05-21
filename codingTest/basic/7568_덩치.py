#68ms
import sys
input = sys.stdin.readline

n = int(input())
bodies = [list(map(int, input().split())) for i in range(n)]
rank = [1]*n

for i in range(n):
    for j in range(i+1,n):
        if bodies[j][0] > bodies[i][0] and bodies[j][1] > bodies[i][1]:
            rank[i] += 1
        elif bodies[j][0] < bodies[i][0] and bodies[j][1] < bodies[i][1]:
            rank[j] += 1

for i in range(n):
    print(rank[i], end = " ")
    
#56ms
num=int(input())
val=[]
for i in range(num) :
    val.append(list(map(int,input().split())))

for i in val :
    rank=1
    for j in val :
        if i[0] < j[0] and i[1] < j[1]:
                rank += 1
    print(rank,end=' ')