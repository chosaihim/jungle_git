import sys, math

def primeTable(input):
    pt = [1 for i in range(input)] #pt = prime Table

    pt[0] = 0; pt[1] = 0

    for number in range(3, input):
        for devider in range(3, int(math.sqrt(input))):
            if(number%2==0): pt[number]=0
            else:
                if(pt[number]==0):
                    continue
                else:
                    for num in range(2*number,input, number):
                        pt[num] = 0
    return pt


#main
primes = primeTable(10001)

t = list(map(int, sys.stdin.readline().split()))[0]

for i in range(t):
    input = list(map(int, sys.stdin.readline().split()))[0]

    goldbachs = []

    for i in range(int(input/2+1)):
        if(primes[i]):
            if(primes[input-i]):
                goldbachs.append(i)

    min = 10000
    for i in range(len(goldbachs)):
        if(min > input-goldbachs[i]):
            min = input-goldbachs[i]
            answer1 = goldbachs[i]
            answer2 = input-goldbachs[i]
    
    print(answer1, answer2)
