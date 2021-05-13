#https://www.acmicpc.net/problem/11816

import sys
x = input()

# def x_num(x):
#     ret = 0
    
#     if x[0] != '0':
#         return x      
#     else:
#         if len(x) == 1:
#             return x
#         else:
#             if x[1] == 'x':
#                 power = 1
#                 for i in range(len(x)-1,1,-1):
#                     # print(f'i:{i}, x[{i}]={x[i]}')
#                     if(ord(x[i])>96):
#                         # print(f'{i} alphabet: {x[i]}')
#                         ret += (ord(x[i])-87) * power
#                     else:
#                         # print(f'{i} digit: {x[i]}')
#                         ret += int(x[i]) * power
#                     power *= 16
                        
#             else:
#                 power = 1
#                 for i in range(len(x)-1,-1,-1):
#                     ret += int(x[i]) * power
#                     power *= 8
                    
#     return ret

def octToDec(x):
    return int(x[1:],8)
def hexToDec(x):
    return int(x[2:],16)
def convert(x):
    if(x[0:2] == "0x"):
        return hexToDec(x)
    elif(x[0] == "0"):
        return octToDec(x)
    else:
        return x
    

print(convert(x))

### 정답!!
## t=input();c=[[0,1][t[0]=='0'],2][t[1]=='x'];print(int(t[c:],[10,8,16][c]))