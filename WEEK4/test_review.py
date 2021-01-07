"import sys


def solve():
    n = int(sys.stdin.readline().strip())
    
    stair_list = []
    for i in range(n):
        stair_list.append(int(sys.stdin.readline().strip()))
    
    # dp는 2*n+1 행렬
    dp = [[0]*(n + 1) for _ in range(2)]
    dp[0][1] = stair_list[0]
    for i in range(2, n + 1):
        # 0으로 가는 법
        dp[0][i] = max(dp[0][i - 2], dp[1][i - 2]) + stair_list[i - 1]
        # 1로 가는 법
        dp[1][i] = dp[0][i - 1] + stair_list[i - 1]

    ans = max(dp[0][-1], dp[1][-1])
    return ans


print(solve())
"

"import sys
sys.setrecursionlimit(2000)


def solve():
    # 항상 낮은 지점으로만 가니까 visited 필요 없음
    # 이 지점에서 갈 수 있는 개수만 기록하면 됨
    # dfs를 돌고 여기서 갈 수 있는 개수를 저장하자
    # 이미 간 길에 도착하면 그 값을 반환하자
    def dfs(start):
        if start == (m - 1, n - 1):
            return 1

        count = 0
        for di in direc:
            temp = -1
            new_pos = (start[0] + di[0], start[1] + di[1])
            # new_pos에 갈 수 있다면
            if 0 <= new_pos[0] < m and 0 <= new_pos[1] < n and map_list[new_pos[0]][new_pos[1]] < map_list[start[0]][start[1]]:
                # new_pos가 이미 탐색이 끝났다면
                if dp[new_pos[0]][new_pos[1]] != -1:
                    temp = dp[new_pos[0]][new_pos[1]]
                else:
                    temp = dfs(new_pos)
            if temp != -1:
                count += temp
        
        dp[start[0]][start[1]] = count
        return count
    m, n = map(int, sys.stdin.readline().strip().split())

    map_list = []
    for _ in range(m):
        map_list.append(list(map(int, sys.stdin.readline().strip().split())))
    
    dp = [[-1]*n for _ in range(m)]
    direc = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    dfs((0, 0))
    return dp[0][0]


print(solve())
"

"import sys
import queue
import bisect

# 무게당 value로 정렬하기 vs value로 정렬하기
# 그냥 value로 정렬하는게 맞지 않을까 ?
# value 가장 큰 것부터 겨우 겨우 들어가는 가방에 넣자
# 가방이 1하고 100만 있고 (2, 50)짜리 보석이랑 (100, 100)짜리 보석이 있으면 누굴 넣어야 하지?
# 무적권 100짜리 넣어야지 ㅇㅇ 이건 맞지
# 시간초과

def solve():
    n, k = map(int, sys.stdin.readline().strip().split())

    heap = queue.PriorityQueue()
    bag_list = []
    for _ in range(n):
        m, v = map(int, sys.stdin.readline().strip().split())
        # 우선순위큐에 v를 기준으로 내림차순 정렬하자
        heap.put((-v, m))
    for _ in range(k):
        bag_list.append(int(sys.stdin.readline().strip()))
    
    bag_list.sort()
    
    ans = 0
    for i in range(heap.qsize()):
        cur_v, cur_m = heap.get()
        min_bag = bisect.bisect_left(bag_list, cur_m)
        if min_bag == len(bag_list):
            continue
        else:
            del bag_list[min_bag]
            ans -= cur_v
    
    return ans

print(solve())
"