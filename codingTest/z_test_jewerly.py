import sys
import math
from collections import defaultdict

n, r, c = map(int, sys.stdin.readline().split())

graph = defaultdict(int)
graph[(0,0)] = 0

def divide_conquer(n, i, j):
    if n == 2:
        for x, y, plus in [(0,1, 1), (1,0, 2), (1,1, 3)]:
            nx = i + x
            ny = j + y
            graph[(nx, ny)] = graph[(i,j)] + plus
    else:
        first_plus = pow(2, (n//2))
        for x, y, plus in [(0,0,0), (0,n//2, first_plus), (n//2,0, first_plus*2), (n//2,n//2, first_plus*3)]:
            nx = i + x
            ny = j + y
            if nx <= r < nx + n//2 and ny <= c < ny + n //2 :
                graph[(nx, ny)] = graph[(i,j)] + plus
                divide_conquer(n//2, nx, ny)
            
divide_conquer(pow(2,n), 0, 0)

print(graph[(r,c)])



#태양
import sys  
sys.setrecursionlimit(10**8)
n,r,c = map(int,sys.stdin.readline().rstrip().split())

def partition(_r:int, _c:int):
    if _r <= 1 and _c <= 1:
        return 2*_r + _c
    for k in range(int(n),0,-1):
        if _r >= pow(2,k) and _c >= pow(2,k) :
            return partition(_r-pow(2,k), _c-pow(2,k)) + pow(2, 2*k+1) + pow(2, 2*k)
        elif _r >= pow(2,k):
            return partition(_r-pow(2,k), _c) + pow(2, 2*k+1)
        elif _c >= pow(2,k):
            return partition(_r, _c-pow(2,k))+ pow(2,2*k) 

print(partition(r,c))