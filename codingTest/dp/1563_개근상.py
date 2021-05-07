import sys
sys.setrecursionlimit(10**6)

N=int(input())

cache = [[[-1]*3 for _ in range(2)] for _ in range(N + 1)]

def attendance(day, late, absent):
    
    if late == 2 or absent == 3: return 0
    if day == N: return 1
    if cache[day][late][absent] != -1: return cache[day][late][absent]
    else:
        attend = attendance(day+1, late, 0) + attendance(day+1, late+1, 0) + attendance(day+1, late, absent+1)
        cache [day][late][absent] = attend

    return attend

print(attendance(0,0,0) % 1000000)
