import sys

## main
n = list(map(int, sys.stdin.readline().split()))[0]

answer = 0
if n < 100:
    answer = n
    
else:
    answer = 99
    
    for i in range(1,int(n/100)+1):
        # print(i*100, "*******")
        for j in range(-5,5):
            # print("j: ", j)
            if ((i+2*j) < 0):
                continue
            elif (i+2*j)>9:
                break
            elif(i*100 + (i+j)*10 + (i+2*j)) <= n:                
                # print("hansoo: ", i*100 + (i-j)*10 + (i-2*j))         
                answer += 1
            else:
                break
        
print(answer)