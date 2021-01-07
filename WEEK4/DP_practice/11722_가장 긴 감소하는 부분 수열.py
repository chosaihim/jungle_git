import sys
input = sys.stdin.readline

N = int(input())
arr = list(map(int,input().split()))
cache = [0] * N

def part(n):
    # print(f'into {n}')
    if(n == 0): return 1

    if cache[n]: return cache[n]

    max_value = 1
    for i in reversed(range(n)):
        if arr[i] > arr[n]:
            temp = part(i) +1
            max_value = max(max_value,temp)
    cache[n] = max_value

    return max_value

max_v = 0
for i in range(N):
    max_v = max(max_v, part(i))

print(max_v)

