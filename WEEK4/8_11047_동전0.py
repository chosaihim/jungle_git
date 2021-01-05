import sys
input = sys.stdin.readline

N, goal = map(int, input().split()) # N: number of coins, K:goal value
coins = [int(input()) for _ in range(N)]

total = 0
coin_cnt = 0
for coin in reversed(coins):
    left = goal-total
    if coin <= left:
        cnt = left//coin
        total += coin * cnt
        coin_cnt += cnt

print(coin_cnt)



    # while True:
    #     if coin <= (goal - total):
    #         total += coin
    #         coin_cnt += 1
    #     else: break