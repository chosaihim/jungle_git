import sys
input = sys.stdin.readline
sys.setrecursionlimit(10**9)

N, K = map(int, input().split()) # N: number of items, K: maximum wieght K(1 ≤ K ≤ 100,000)
items = [list(map(int, input().split())) for _ in range(N)] # W: 무게 V:가치 [W,V] W(1 ≤ W ≤ 100,000)

items.sort()                    # 무게별로 Sort 해두고
min_weight = items[0][0]        # 가장 가벼운 무게 찾기
items.sort(key=lambda x:x[1])   # value별로 한 번 더 sort

print(items)

visited = []
# visited.append(items[-1])

max_values_by_weight =[0]*(K+1)
# min_weight = items[0][0]
print(f'min_weight: {min_weight}')

def packing(weight): # return max value

    print(f'weight:{weight}')

    max_value = 0

    if   weight <  min_weight: return 0
    # elif weight == min_weight: print("2"); visited.append(items[0]); return items[0][1]
    
    if max_values_by_weight[weight]: return max_values_by_weight[weight]

    # print(f'items before for: {items}')
    for item in items:
        value = 0
        if item[0] > weight: continue
        elif item not in visited:
            print(f'  >>  will be added: [{item[0]}kg, {item[1]} worthy, left = {weight-item[0]}]')
            # print(item)
            visited.append(item)
            value = packing(weight-item[0]) + item[1]
            visited.pop()
            max_value = max(max_value, value)
            print(f'returned from {weight-item[0]} value:{value}, max_value:{max_value} in {weight}kg')

    max_values_by_weight[weight] = max_value
    print(f'  >>  max_value:{max_value}, max_Value_by_weight: {max_values_by_weight}')
    return max_value

print(packing(K))