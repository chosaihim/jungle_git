import sys
input = sys.stdin.readline
sys.setrecursionlimit(10**6)

### INPUT
N, M = map(int, input().split()) # N(2 ≤ N ≤ 10,000): num of stones, M(0 ≤ M ≤ N-2): num of small
smalls = [int(input())-1 for _ in range(M)]
smalls.sort()

# print(f'N:{N}, M:{M}')
# print(f'smalls:{smalls}')
cache = [[0]*(1<<N) for _ in range(N)]
dx = [-1, 0, 1]

def jump(stone_num, jump_dist):

    # print(f'stone_num:{stone_num} with jump:{jump_dist}')
    
    if stone_num == N-1: return 1
    # if stone_num in smalls or stone_num > N: return 10**10

    if cache[stone_num][jump_dist]:return cache[stone_num][jump_dist]

    temp = 10**10
    for d_jump in dx:
        jump_now = jump_dist + d_jump
        next_try = stone_num+jump_now
        # print(f'try to jump to {next_try}')
        if jump_now > 0 and stone_num+jump_now < N and stone_num+jump_now not in smalls:
            temp = min(temp, jump(stone_num+jump_now, jump_now)+1)
    
    cache[stone_num][jump_dist] = temp
    return temp
    # return 1


# print(f'answer: {jump(0,1)}')
# print(jump(1,1))
answer = jump(1,1)
if answer > 10**9: print(-1)
else: print(answer)
    
