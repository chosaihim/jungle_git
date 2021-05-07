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

# dp=[[[-1 for absent in range(3)] for late in range(2)] for day in range(N+1)]
# def dfs(day,late,absent):
#     # 지각2번 or 결석연속3번
#     if late==2 or absent==3:
#         return 0
#     # 개근을한 경우
#     if day==N:
#         return 1

#     if dp[day][late][absent]==-1:
#         # 참석 + 지각 + 결석
#         attend=dfs(day+1,late,0)+dfs(day+1,late+1,0)+dfs(day+1,late,absent+1)
#         dp[day][late][absent]=attend

#         return attend
#     else:
#         return dp[day][late][absent]
            
# ans=0
# print((dfs(0,0,0))%1000000)

# import sys
# input = sys.stdin.readline

# n = int(input())

# dp = [0] * n
# ddp = [[1]*3 for _ in range(n+1)]

# # day 2
# if n > 1:
# d[1][0][0] = 1
# d[1][0][1] = 1
# d[1][0][2] = 1
# d[1][1][0] = 3
# d[1][1][1] = 1

# if n > 2:

# for d in range(1,n):
#     ddp[d][0][0] = ddp[d-1][0][0]
#     ddp[d][1][0] = ddp[d-1][1][0] + ddp[d-1][0][0]
#     ddp[d][0][1] = ddp[d-1][0][1] + ddp[d-1][0][0]
#     ddp[d][0][2] = ddp[d-1][0][2] + ddp[d-1][0][1]
#     ddp[d][1][1] = ddp[d-1][1][1] + ddp[d-1][1][0] + ddp[d-1][0][1]
#     ddp[d][1][2] = ddp[d-1][1][2] + ddp[d-1][1][1] + ddp[d-1][0][2]
    
#     print(ddp)
