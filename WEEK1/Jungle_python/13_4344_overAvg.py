import sys  
n = list(map(int, sys.stdin.readline().split()))[0]

rate = []

for i in range(n):
    cnt = 0
    
    scores = list(map(int, sys.stdin.readline().split()))
    avg = (sum(scores)-scores[0])/(len(scores)-1)

    for j in range(1,len(scores)):
        if scores[j] > avg :
            cnt = cnt + 1

    rate.append(cnt/((len(scores)-1)))

for i in range(n):
    print(format(rate[i], ".3%"))