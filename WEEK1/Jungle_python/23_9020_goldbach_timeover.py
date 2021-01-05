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

def goldbach(case):
    answer = []
    if(case == 2):
        return answer.append(1)
    for i in range(2,int(case/2+1)):
        if(isPrime(i)):
            if(isPrime(case - i)):
                answer.append(i)    
    return answer


## main
n = list(map(int, sys.stdin.readline().split()))[0]

cases = []
for i in range(n):
    cases.append(list(map(int, sys.stdin.readline().split()))[0])


for i in range(n):
    ans = goldbach(cases[i])
    answer = 0
    if(len(ans) == 1):
        print(ans[0]," ",cases[i]-ans[0])
    else:
        for j in range(len(ans)):
            if (cases[i]-2*ans[j-1] < cases[i]-2*ans[j]):
                answer = ans[j-1]
            else:
                answer = ans[j]
        print(answer," ", cases[i]-answer)

        # temp = []
        # for j in range(len(ans)):
        #     temp.append(cases[i]-2*ans[j])
        # index = temp.index(min(temp))
        # print(ans[index],end=' ')
        # print(cases[i]-ans[index])