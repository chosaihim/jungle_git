import sys
import math
input = sys.stdin.readline
sys.setrecursionlimit(10**6)

### INPUT
N, M = map(int, input().split()) # N(2 ≤ N ≤ 10,000): num of stones, M(0 ≤ M ≤ N-2): num of small
smalls = [int(input())-1 for _ in range(M)]

# cache = [[0]*int(math.sqrt(4*N)) for _ in range(N)]
cache = [[0]*200 for _ in range(N)]
visited = [0]


dx = [-1, 0, 1]
def jump(stone_num, jump_dist):
    
    if stone_num == N-1: return 1
    if cache[stone_num][jump_dist]: return cache[stone_num][jump_dist]

    temp = 10**5
    if stone_num + jump_dist -1 > N: return temp

    for d_jump in dx:
        jump_now   = jump_dist + d_jump
        stone_next = stone_num + jump_now
        if jump_now > 0 and stone_next < N and stone_next not in smalls:
            temp = min(temp, jump(stone_next, jump_now)+1)
    
    cache[stone_num][jump_dist] = temp
    return temp

answer = jump(1,1)
if answer > 10**5: print(-1)
else: print(answer)
    
