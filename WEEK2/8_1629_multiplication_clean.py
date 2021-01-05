import sys
b_dic = {0:1}

a, b, c = list(map(int, sys.stdin.readline().split()))

def power(a,b,c):
    if(b in b_dic): return b_dic[b]
    
    if(b==0):   return 1
    elif(b==1): b_dic[1]=a; return a
    else:
        temp_power = power(a%c,b//2,c)
        b_dic[b] = (temp_power%c*temp_power%c*power(a%c,b%2,c)%c)%c
        return b_dic[b]

print(power(a%c,b,c))