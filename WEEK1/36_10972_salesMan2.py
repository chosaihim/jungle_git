import sys

cities = int((sys.stdin.readline().split())[0])

costs = []
for city in range(cities):
    cost = list(map(int, sys.stdin.readline().split()))
    costs.append(cost)

arr = [i for i in range(cities)]
cache = []
temp_cost = 0
mini_cost = 10**8

answer = [0]
cache.append(0)

def routes(array, depth, limit):
    global temp_cost
    global mini_cost

    if(depth == limit):
    
        for i in range(len(answer)-1):
            temp_cost += costs[answer[i]][answer[i+1]]
        if costs[answer[-1]][0] :
            temp_cost += costs[answer[-1]][0]
        else:
            temp_cost = 10**8
        
        if(temp_cost < mini_cost):
            mini_cost = temp_cost
        
        temp_cost = 0
        None
    else:
        for i in (array):
            if(i in cache):
                None
            else:
                
                if(costs[answer[-1]][i]):
                    answer.append(i)
                    cache.append(i)
                    routes(array,depth+1,limit)
                    answer.remove(i)
                    cache.remove(i)

                if depth == 0:
                    cache.append(i)

routes(arr, 1, cities)
print(mini_cost)