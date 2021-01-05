import sys
debugFlag = True
# debugFlag = False

color = []
n = list(map(int, sys.stdin.readline().split()))[0]
for i in range(n):
    color.append(list(map(int, sys.stdin.readline().split())))

if(debugFlag):
    for i in range(n):
        print(color[i])

def blue_combine(n,x,y):
    if debugFlag: print(f'n:{n},x:{x},y:{y}')

    com = 0
    area = 0

    if(n == 1):
        return -color[x][y]
    else:
        half_n = n //2 
        area1 = blue_combine(half_n,x,y)
        area2 = blue_combine(half_n,x,y+half_n)
        area3 = blue_combine(half_n,x+half_n,y)
        area4 = blue_combine(half_n,x+half_n,y+half_n)

        if(area1 == area2 == area3 == area4 == -1): area = -1
        else: 
            # area1 = abs(area1); area2 = abs(area2); area3 = abs(area3); area4 = abs(area4);
            area = abs(area1) + abs(area2) + abs(area3) + abs(area4)
        return area

    return area

def white_combine(n,x,y):
    if debugFlag: print(f'n:{n},x:{x},y:{y}')
    com = 0
    area = 0

    if(n == 1):
        if(color[x][y] == 0): return -1
        else: return 0
    else:
        half_n = n //2 
        area1 = white_combine(half_n,x,y)
        area2 = white_combine(half_n,x,y+half_n)
        area3 = white_combine(half_n,x+half_n,y)
        area4 = white_combine(half_n,x+half_n,y+half_n)

        # area = white_combine(half_n,x,y) + white_combine(half_n,x,y+half_n) + white_combine(half_n,x+half_n,y) + white_combine(half_n,x+half_n,y+half_n)
        if(area1 == area2 == area3 == area4 == -1): area = -1
        else: area = abs(area1) + abs(area2) + abs(area3) + abs(area4)
        return area
        return area

    return area

print(abs(white_combine(n,0,0)))
print(abs(blue_combine(n,0,0)))