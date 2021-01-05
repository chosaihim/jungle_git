import sys

## main
w, h = list(map(int, sys.stdin.readline().split()))
cuts = list(map(int, sys.stdin.readline().split()))[0]

horizontal = [0,h]
vertical = [0,w]

for i in range(cuts):
    hOrV, line = list(map(int, sys.stdin.readline().split()))

    if(hOrV == 0):
        horizontal.append(line)
    else:
        vertical.append(line)

horizontal.sort()
vertical.sort()

widths = []
heights = []
for i in range(1,len(horizontal)):
    widths.append(horizontal[i]-horizontal[i-1])

for i in range(1,len(vertical)):
    heights.append(vertical[i]-vertical[i-1])

print(max(widths)*max(heights))