import sys  
n = list(map(int, sys.stdin.readline().split()))[0]

score = 0
total = 0
totals =[]

for i in range(n):
    str = sys.stdin.readline().strip()

    for j in range(len(str)):
        if(str[j] == 'O'):
            score = score + 1
        else:
            score = 0
        
        total = total + score
        
    totals.append(total)
    
    total = 0
    score = 0


for i in range(n):
    print(totals[i])