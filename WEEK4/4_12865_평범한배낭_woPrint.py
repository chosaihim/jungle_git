import sys
input = sys.stdin.readline
sys.setrecursionlimit(10**9)


### INPUT
N, K = map(int, input().split()) # N: number of items, K: maximum wieght K(1 ≤ K ≤ 100,000)
items = [list(map(int, input().split())) for _ in range(N)] # W: 무게 V:가치 [W,V] W(1 ≤ W ≤ 100,000)


### 초기 변수값 세팅
# 1. 가장 가벼운 무게 찾기(그 이하의 무게를 찾으면 0 return 해주려고)
items.sort()                    # 무게별로 Sort 해두고
min_weight = items[0][0]        # 가장 가벼운 무게 찾기
items.sort(key=lambda x:x[1])   # value별로 한 번 더 sort(나중에 디버깅 쉽게하려고)

# 2. 
visited = []
max_values_by_weight =[0]*(K+1) # 가방 무게별로 담을 수 있는 최대 value 값 저장하는 캐시!

### 함수!
# 최대무게(weight)안에서 젤 큰 가치를 가지게 짐싸는 함수. 
# input: 최대로 담을 수 있는 무게 --> output: 최대로 담을 수 있는 가치
def packing(weight): # return max value

    max_value = 0

    if weight <  min_weight: return 0                                       # 젤 가벼운 것보다 가방에 담을 수 있는게 적으면 바로 0 return
    if max_values_by_weight[weight]: return max_values_by_weight[weight]    # 이미 계산해본 값이면 return

    for item in items:
        if item[0] <= weight and item not in visited:                       # 가방에 넣은 적 없는 아이템을 하나씩 가방에 넣어본다!
            visited.append(item)                                            # 가방에 넣은 샘 치고 visited에 체크
            value = packing(weight-item[0]) + item[1]                       # 지금 넣은 아이템의 가치 + 그 이하 무게에서 담을 수 있는 최대 value
            visited.pop()                                                   # 담에 또 써야하니깐 가방에서 뺀 건 visited uncheck
            max_value = max(max_value, value)                               # 현재까지 중에 젤 큰 value를 max value로 update

    max_values_by_weight[weight] = max_value                                # 이 무게에서 담을 수 있는 가장 큰 가치는 이겁니다! 라고 저장

    return max_value                                                        # 최고 value를 return


### 실행
print(packing(K))
print(max_values_by_weight)