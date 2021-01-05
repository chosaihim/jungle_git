import sys

n_shooting, n_animal, shoot_len = list(map(int, sys.stdin.readline().split()))
shoot_points = list(map(int, sys.stdin.readline().split()))
shoot_points.sort()

def isShootable(a,b):
    global shoot_points
    global shoot_len

    if(b > shoot_len): return False
    elif(b == shoot_len):
        if(a in shoot_points): return True
    else:
        pl = 0                      # 검색 범위의 맨 앞 원소 인덱스
        pr = len(shoot_points) - 1  # 검색 범위의 맨 끝 원소의 인덱스

        while True:
            pc = (pl+pr)//2         #중앙 원소의 인덱스
            if abs(shoot_points[pc]-a) <= abs(shoot_len -b):    
                return True         #검색 성공
            elif shoot_points[pc] < a - abs(shoot_len -b):   
                pl = pc + 1         # 검색 범위를 뒤쪽 절반으로
            else:               
                pr = pc -1          # 검색 범위를 앞쪽 절반으로
            if pl > pr:
                break
    return False

cnt = 0
for _ in range(n_animal):
    animal = list(map(int, sys.stdin.readline().split()))

    if(isShootable(animal[0], animal[1])): cnt += 1

print(cnt)