import sys
input = sys.stdin.readline

n, k = map(int, input().split())
coins = list(int(input()) for _ in range(n))
coins.sort()
print(coins)
