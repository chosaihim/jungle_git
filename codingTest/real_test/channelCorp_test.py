import sys
sys.setrecursionlimit(10**6)

def solution(n):
    answer = 1
    
    def find_comb(goal, nums):
        ret = []
        
        if nums > goal: nums = goal
        
        if goal == 1: return [[1]]
        if nums == 1: return [[goal]]
        
        else:
            for i in range(goal//nums + 1):
                comb_ret = find_comb(goal-i,nums-1)
                for c in comb_ret:
                    ret.append([i]+c)
        return ret

    
    list_comb = list(find_comb(n,n))
    print(list_comb)
    
    max_total = 0
    for comb in list_comb:
        total = 1
        for c in comb:
            if c != 0:
                total *= c
        max_total = max(max_total, total)
    
    answer = max_total
        
    return answer

print(solution())