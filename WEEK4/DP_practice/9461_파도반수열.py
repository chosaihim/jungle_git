import sys
input = sys.stdin.readline



T = int(input())
for test in range(T):
    n = int(input())
    
    cache = [0] * (n+1)
    
    def P(n):
        if n == 1: return 1
        elif n == 2: return 1
        elif n == 3: return 1
        
        if cache[n]: return cache[n]

        cache[n] = P(n-2) + P(n-3)
        return cache[n] 

    print(P(n))
