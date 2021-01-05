import sys
input = sys.stdin.readline

n = int(input())    # n: number of cities
costs = [list(map(int, input().split())) for i in range(n)]

def tsp(costs):
    # 초기변수값 설정
    N = len(costs)              # 전체 도시 개수 = n
    VISITED_ALL = (1<<N)-1      # 다 1로 채워서 다 방문 상태로 만들어준 값
    cache = [[None] * (1<<N) for _ in range(N)] 
    INF = float('inf')          # INFINITY 세팅

    def find_path(last, visited):
        if visited == VISITED_ALL:
            return costs[last][0] or INF
        
        if cache[last][visited] is not None:
            return cache[last][visited]

        tmp = INF

        for city in range(N):
            if visited & (1<<city) == 0 and costs[last][city] != 0:
                tmp = min(tmp, find_path(city, visited | (1<<city)) + costs[last][city])
        cache[last][visited] = tmp
        return tmp

    return find_path(0, 1<<0)



print(tsp(costs))