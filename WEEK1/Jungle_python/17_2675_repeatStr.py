import sys  
n = list(map(int, sys.stdin.readline().split()))[0]

answer = []

for i in range(n):
    repeat, string = list(map(str, sys.stdin.readline().split()))
    
    temp = ""

    for j in range(len(string)):
        for k in range(int(repeat)):
            temp = temp + string[j]
    
    answer.append(temp)

for i in range(n):
    print(answer[i])