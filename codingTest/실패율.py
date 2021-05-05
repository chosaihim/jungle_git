import sys
input = sys.stdin.readline

def solution(N, stages):
    answer = []
    
    trials = [0] * (N+2)
    stays = [0] * (N+2)
    
    for stage in stages:
        for i in range(stage+1):
            trials[i] += 1
        stays[stage] += 1
    
    fail_rate = []
    for i in range(1,N+1):
        if trials[i] == 0: fail_rate.append([i,0])
        else: fail_rate.append([i,stays[i]/trials[i]])

    fail = sorted(fail_rate, key = lambda x:(-x[1], x[0]))

    for f in fail: answer.append(f[0])
    return answer




#output
N = 5
stages = [2, 1, 2, 6, 2, 4, 3, 3]
print(solution(N, stages))


# 풀이
# def solution(N, stages):
#     result = {}
#     denominator = len(stages)
#     for stage in range(1, N+1):
#         if denominator != 0:
#             count = stages.count(stage)
#             result[stage] = count / denominator
#             denominator -= count
#         else:
#             result[stage] = 0
#     return sorted(result, key=lambda x : result[x], reverse=True)

# 풀이 2
def solution(N, stages):
    fail = {}
    for i in range(1,N+1):
        try:
            fail_ = len([a for a in stages if a==i])/len([a for a in stages if a>=i])
        except:
            fail_ = 0
        fail[i]=fail_
    answer = sorted(fail, key=fail.get, reverse=True)
    return answer