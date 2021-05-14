import sys
input = sys.stdin.readline

n = int(input())
slate = [list(map(int,input().split())) for _ in range(n)]

print(slate)

