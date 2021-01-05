import sys

def isPrime(input):
    if(input==0 or input == 1):
        return False
    elif(input ==2):
        return True
    elif input % 2 == 0:
        return False
    else:
        for i in range(2,input):
            if(i%2==0):
                continue
            elif(input%i==0):
                return False            
    return True


## main
n = list(map(int, sys.stdin.readline().split()))[0]
inputs = list(map(int, sys.stdin.readline().split()))

cnt = 0
for i in range(n):
    if(isPrime(inputs[i])):
        cnt = cnt +1
print(cnt)
