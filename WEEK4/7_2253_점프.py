import sys
input = sys.stdin.readline
from collections import deque

### INPUT
N, M = map(int, input().split()) # N(2 ≤ N ≤ 10,000): num of stones, M(0 ≤ M ≤ N-2): num of small
small = [0] * N
for _ in range(M): small[int(input())-1] = 1 #전체 돌 중에서 작은 애들만 1 넣어줌. 나머지는 0

## 변수 세팅
cache = [[0]*200 for _ in range(N)]
dx = [-1, 0, 1]

## BFS
def bfs(_root, _jump, _depth):
    queue = deque()
    queue.append([_root,_jump,_depth])
    cache[_root][_jump] = 1

    while queue:
        v, jump, depth = queue.popleft()

        if v == N-1: return depth

        if v + jump - 1 < N:
            for d_jump in dx:
                jump_now = jump + d_jump
                next_stone = v + jump_now
                if jump_now > 0 and next_stone < N and not small[next_stone] and not cache[v][jump_now]:
                    queue.append([next_stone,jump_now,depth+1])
                    cache[v][jump_now] = 1

## 실행
answer = bfs(1,1,1)
if answer is None: print(-1)
else: print(answer)
        