repeat = int(input())
import math

case = []
for i in range(repeat):
    case.append(int(input()))

ansCaseArray =[]
ansArray =[]

#case 횟수 별로 돌림
for caseidx in range(len(case)):
    for i in range(11):
        if case[caseidx] == 0:
            break
        ansArray.append(1)
        case[caseidx] -= 1
        
    
repeat = int(input())

case = []
for i in range(repeat):
    case.append(int(input()))

possibleCase = []

ways = 0
def waysToGetNumer(num):
    global ways
    threes = num//3
    twos = num//2
    ones = num
    for three in range(threes, -1, -1):
        for two in range(twos, -1, -1):
            for one in range(ones, -1, -1):
                rest = num - 3*three
                rest = rest - 2*two
                rest = rest - one
                # if rest < 0:
                #     continue
                if rest == 0:
                    # print(['3'*three, '2'*two, '1'*one])
                    possibleCase.append(['3'*three, '2'*two, '1'*one])
    
    for i in range(len(possibleCase)):
        case = ''.join(possibleCase[i])
        caselength = len(case)
        ways += math.factorial(caselength) / (math.factorial(len(possibleCase[i][0]))*math.factorial(len(possibleCase[i][1]))*math.factorial(len(possibleCase[i][2])) )
        


for i in range(repeat):
    waysToGetNumer(case[i])
    print(int(ways))
    
    ways = 0    
    possibleCase = []