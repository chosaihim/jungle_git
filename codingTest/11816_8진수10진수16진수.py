#https://www.acmicpc.net/problem/11816

import sys
x = input()

def x_num(x):
    ret = 0
    
    print("len:", len(x))
    
    if x[0] != '0':
        return x      
    else:
        if len(x) == 1:
            return x
        else:
            if x[1] == 'x':
                # print(f'a = {ord("a")}')
                # if(ord(x[2])>96):
                    # print("this is alphabet")
                # else:
                    # print("this is digit")
                # ret = int(x[2])
                power = 1
                for i in range(len(x)-1,1,-1):
                    print(f'i:{i}, x[{i}]={x[i]} || {x.isalpha}')
                    if(x[i].isalpha):
                        print(f'{i} alphabet: {x[i]}')
                        ret += (ord(x[i])-87) * power
                    else:
                        print(f'{i} digit: {x[i]}')
                        ret += int(x[i]) * power
                    power *= 16
                        
            else:
                power = 1
                for i in range(len(x)-1,-1,-1):
                    ret += int(x[i]) * power
                    power *= 8
                    
    return ret

print(x_num(x))