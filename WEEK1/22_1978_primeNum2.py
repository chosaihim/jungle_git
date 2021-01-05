import sys

def isPrime(input):
    l = [1 for i in range(input)]
    
    if(input==0 or input == 1):
        return False
    elif(input ==2):
        return True
    elif input % 2 == 0:
        return False
    else:
        for i in range(3,input):
            if(l[i] == 0):
                continue
            else:
                if(input % i == 0):
                    return False
                else:
                    for j in range(i,input,i):
                        if(l[j] == 0):
                            continue
                        else:
                            l[j] = 0
                            
    return True


## main
n = list(map(int, sys.stdin.readline().split()))[0]
inputs = list(map(int, sys.stdin.readline().split()))

cnt = 0
for i in range(n):
    if(isPrime(inputs[i])):
        cnt = cnt +1
print(cnt)
