import sys
from itertools import combinations
input = sys.stdin.readline

n = int(input())
hallway = [list(map(str, input().split())) for _ in range(n)]

# 장애물을 놓을 수 있는 위치 array에 넣기
obstacle_map = []
teachers = []
for row in range(n):
    for col in range(n):
        if hallway[row][col] == 'X':
            obstacle_map.append([row, col])
        elif hallway[row][col] == 'T':
            teachers.append([row,col])

# 장애물 3개 놓을 수 있는 조합 찾기
comb_obstacles = list(combinations(obstacle_map,3))

d_row = [0, 1, 0, -1]
d_col = [1, 0, -1, 0]

# 선생님 시야: 학생 걸리면 return false
def teacherSight(hallway,teahcers):
    for teacher in teachers:
        row, col = teacher
        
        for d in range(4):
            r = row + d_row[d]; c = col + d_col[d]
            
            while 0 <= r < n and 0 <= c < n:
                if hallway[r][c] == 'O' or hallway[r][c] == 'T':
                    break
                elif hallway[r][c] == 'S':
                    return False
                r += d_row[d]; c += d_col[d]
    return True

# 피했어? return YES or NO
def avoid(hallway, comb_obstacles, teachers):

    for obstacles in comb_obstacles:
        for obstacle in obstacles:
            hallway[obstacle[0]][obstacle[1]] = 'O'   
        
        result = teacherSight(hallway, teachers)
        if(result): return "YES"
        
        for obstacle in obstacles:
            hallway[obstacle[0]][obstacle[1]] = 'X'
    
    return "NO"

# 정답출력
print(avoid(hallway, comb_obstacles, teachers)) 