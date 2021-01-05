import sys
from collections import deque
input = sys.stdin.readline


cache = [0] * 91

n = int(input())

def fibonacci(n):
    # print(f'fibonacci({n})')
    if n <2: return n  
    
    if cache[n]: return cache[n]
    else:
        cache[n] = fibonacci(n-1) + fibonacci(n-2)
        return cache[n]

print(fibonacci(n))