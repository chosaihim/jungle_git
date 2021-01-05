import sys

n = list(map(int, sys.stdin.readline().split()))[0]
arr = list(map(int, sys.stdin.readline().split()))        #input sequence a
cost = [1 for i in range(n)]


def dp(n):
    temp_cost = 0

    if(n == 0): return 1; 
    if(cost[n] > 1): return cost[n]
    else:    
        max_cost = 0
        for i in reversed(range(0,n)):
            if(arr[i]<arr[n]):
                dp_temp = dp(i)
                cost[n] = max(cost[n],dp_temp + 1)

    return cost[n]

for i in range(len(arr)):
    dp(i)
print(max(cost))