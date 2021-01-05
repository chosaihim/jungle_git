import sys
input = sys.stdin.readline

n = int(input())    # n: number of cities
costs = [list(map(int, input().split())) for i in range(n)]

cache = [[0]*(1<<n) for _ in range(n)]


def travel(start, visited):
    
    if visited == ((1<<n)-1):
        if costs[start][0] != 0 :return costs[start][0]
        else: return 10**10
    if cache[start][visited]: return cache[start][visited]
    
    temp = 10**10
    for city in range(n):
        if visited & (1<<city) == 0 and costs[start][city] != 0:
            temp = min(temp, travel(city, visited | (1<<city))+costs[start][city])
    
    cache[start][visited] = temp
    return temp

print(travel(0, 1<<0))