import sys
from itertools import permutations
input = sys.stdin.readline

n = int(input())
a_list = list(map(int,input().split()))
operates_list = list(map(int,input().split()))

oper_list = []
for i in range(4):
    for _ in range(operates_list[i]):
        oper_list.append(i)
p_operates = list(set(permutations(oper_list)))

max_total =  -10000000001
min_total =   10000000001
cache = []
for operates in p_operates:
        total = a_list[0]
        for i in range(len(a_list)-1):
            if operates[i] == 0:
                total += a_list[i+1]
            elif operates[i] == 1:
                total -= a_list[i+1]
            elif operates[i] == 2:
                total *= a_list[i+1]
            elif operates[i] == 3:
                if(total < 0 and a_list[i+1]> 0): total = -((-total) // a_list[i+1])
                elif(total > 0 and a_list[i+1] < 0): total = -(total // (-a_list[i+1]))
                else: total //= a_list[i+1]

        
        if total > max_total: max_total = total
        if total < min_total: min_total = total

    
print(max_total)
print(min_total)
    
    