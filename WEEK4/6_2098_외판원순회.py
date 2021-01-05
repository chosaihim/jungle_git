import sys
input = sys.stdin.readline

n = int(input())    # n: number of cities
costs = [list(map(int, input().split())) for i in range(n)]