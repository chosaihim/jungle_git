import sys
input = sys.stdin.readline


def solution(expression):
    answer = 0
    return answer


print(solution())


#1
def solution(b):
    import math
    
    answer = -1
    
    for a in range(1,b+1):
        c = math.sqrt(a*a + b*b)
        if c == int(c) and b <= c <= 500000:
            return c
    
    return answer

#2
from collections import deque

def solution(n, m, goal_x, goal_y):
    answer = -1
    
    ori_x = [1,0,-1,0]
    ori_y = [0,-1,0,1]
    visited = [[[0 for ori in range(4)] for y_axis in range(m+2)] for x_axis in range(n+2)]
    
    queue = deque([[0,0,0,0]]) # x, y, orientation, depth
    visited[0][0][0] = 1
    
    while queue:
        x, y, ori, depth = queue.popleft()
        
        if x == goal_x and y == goal_y: return depth
        
        # new orientation
        new_ori = (ori+1) % 4
        # new position
        new_x = [x + ori_x[ori], x + ori_x[new_ori], x]
        new_y = [y + ori_y[ori], y + ori_y[new_ori], y]
        
        for i in range(3):
            if 0 <= new_x[i] <= n and 0 <= new_y[i] <= m:
                if visited[new_x[i]][new_y[i]][new_ori] == 0:
                    visited[new_x[i]][new_y[i]][new_ori] =1
                    queue.append([new_x[i], new_y[i], new_ori, depth+1])
        
    return answer

#3
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
            for i in range(goal//nums+1):
                comb_ret = find_comb(goal-i,nums-1)
                for c in comb_ret:
                    ret.append([i] + c)
        return ret

    
    list_comb = list(find_comb(n,n))
    
    max_total = 0
    for comb in list_comb:
        total = 1
        for c in comb:
            if c != 0:
                total *= c
        max_total = max(max_total, total)
    
    answer = max_total
        
    return answer

#4
def solution(n, k, bulbs):
    answer = -2
    
    def switch(color):
        if   color == "R": return "G"
        elif color == "G": return "B"
        elif color == "B": return "R"
    return answer

#5
-- 코드를 입력하세요
SELECT case_counts as "후기 수", COUNT(counts) as "공간 수"
FROM
(
    select
        CASE
            when counts = 0 then '0'
            when counts between 1 and 49 then '< 50'
            when counts between 50 and 99 then '< 100'
            else '>= 100'
        END as case_counts,
        counts
    FROM
    (
        SELECT IFNULL(counts,0) as counts, A.ID AS place
        FROM PLACES AS A
        LEFT OUTER JOIN(
            SELECT PLACE_ID, COUNT(COMMENTS) as counts
            FROM PLACE_REVIEWS
            GROUP BY PLACE_ID
            ORDER BY COUNT(COMMENTS)
        ) AS B ON A.ID = B.PLACE_ID
    ) C
) D
GROUP BY case_counts
ORDER BY field(case_counts,'0','< 50','< 100','>= 100');
