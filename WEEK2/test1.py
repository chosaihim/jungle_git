import sys

video = []
n = list(map(int, sys.stdin.readline().split()))[0]
for i in range(n):
    pixels = list(map(str, sys.stdin.readline().split()))[0]

    line = []
    for i in range(len(pixels)):
        line.append((pixels[i]))
    video.append(line)


def quadTree(n,x,y):
    
    if(n == 1):
        return video[x][y]
    else:
        half_n = n //2 
        area1 = quadTree(half_n,x,y)
        area2 = quadTree(half_n,x,y+half_n)
        area3 = quadTree(half_n,x+half_n,y)
        area4 = quadTree(half_n,x+half_n,y+half_n)

        if(area1 == area2 == area3 == area4 == '1'): return '1'
        elif(area1 == area2 == area3 == area4 == '0'): return '0'
        else: 
            return '(' + area1 + area2 + area3 + area4 + ')'


print(quadTree(n,0,0))