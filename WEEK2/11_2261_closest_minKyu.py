# 가장 가까운 두 점
import sys
input = sys.stdin.readline
def distance(a, b):
    return (a[0]-b[0])**2 + (a[1]-b[1])**2
def solve(start, end):
    if start >= end:
        return float('inf')
    if end - start == 1:
        return distance(coords[end], coords[start])
    mid = (start+end)//2
    d = min(solve(start, mid),
            solve(mid+1, end))
    candidate = []
    for i in range(start, end+1):
        dx = coords[i][0] - coords[mid][0]
        if dx**2 < d:
            candidate.append(coords[i])
    candidate.sort(key=lambda x: x[1])
    for i in range(len(candidate)-1):
        for j in range(i + 1, len(candidate)):
            dy = candidate[i][1] - candidate[j][1]
            if dy**2 < d:
                d = min(d, distance(candidate[i], candidate[j]))
            else:
                break
    return d
sys.setrecursionlimit(5000)
N = int(input())
coords = [list(map(int, input().split())) for _ in range(N)]
coords.sort(key=lambda coord: coord[0])
print(solve(0, N-1))