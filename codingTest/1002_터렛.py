import sys
input = sys.stdin.readline
import math

T = int(input())

def find_enemy(x1, y1, r1, x2, y2, r2):
    
    distance = math.sqrt((x1-x2)**2 + (y1-y2)**2)
    
    if x1 == x2 and y1 == y2:
        if r1 == r2: return -1
        else: return 0
    if r1 + distance <  r2 or r2 + distance <  r1: return 0
    if r1 + distance == r2 or r2 + distance == r1: return 1
    if r1 + r2 <  distance: return 0
    if r1 + r2 == distance: return 1
    return 2
    
for _ in range(T):
    x1, y1, r1, x2, y2, r2 = map(int, input().split())
    print(find_enemy(x1,y1,r1,x2,y2,r2))
