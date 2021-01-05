from heapq import heappop, heappush
import sys
input = sys.stdin.readline

N = int(input())
routes = [sorted(list(map(int, input().split()))) for _ in range(N)]
d = int(input())
routes.sort(key=lambda x: x[1])
heap = []


def solve(d):
    result = 0
    for route in routes:
        heappush(heap, route[0])

        while heap:
            if route[1] - heap[0] > d:
                heappop(heap)
            else:
                break
        result = max(result, len(heap))
    return result


print(solve(d))
