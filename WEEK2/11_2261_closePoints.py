import sys
# debugFlag = True
debugFlag = False

n = list(map(int, sys.stdin.readline().split()))[0]

points =[]
for _ in range(n):
    # x,y = list(map(int, sys.stdin.readline().split()))
    points.append(list(map(int, sys.stdin.readline().split())))

    points.sort()

print(points)

