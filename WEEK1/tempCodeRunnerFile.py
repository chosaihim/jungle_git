import sys

def isSafe(n,x,y,waterlevel):
    if(0<=x<n and 0<=y<n):
        if(water_zone[x][y] == 1):      #지금 들어온 구역이 안전구역이면 검사 시작!
            water_zone[x][y] = 2        #water zone에 해당 구역 체크
            isSafe(n, x-1,y  ,waterlevel)   # 왼쪽
            isSafe(n, x+1,y  ,waterlevel)   # 오른쪽
            isSafe(n, x  ,y+1,waterlevel)   # 아래 로 검사구역 확장! (젤 위부터 시작해서 위는 검사할 필요 x)
            return None
        else:
            return None

# nxn행렬에서 수위가 waterlevel일 때, 
def countZones(n,waterlevel):
    zone_cnt = 0
    for y in range(n):                      # 한 줄 씩 검사   
        for x in range(n):                  # 한칸씩 옆으로 이동해가면서
            if(water_zone[x][y] == 1):
                isSafe(n,x,y,waterlevel)
                zone_cnt += 1
            else: continue
    
    return zone_cnt


# main
# N: 2차원 배열의 행과 열의 개수
n = int((sys.stdin.readline().split())[0])
zones = []
water_zone = [[1 for i in range(n)] for j in range(n)]

# 각 땅의 높이 받아오기
for i in range(n):
    zone = list(map(int, sys.stdin.readline().split()))
    zones.append(zone)

# 땅 중에서 가장 높은 곳?
max_zone = max(max(zones))
max_cnt = 0


# 수위를 하나씩 높이면서 안전지역 개수세기
for waterlevel in range(max_zone):

    #water_zone 만들기 (물에 잠긴 지역 표시: 0잠김 1안전)    
    for row in range(n):
        for col in range(n):
            water_zone[row][col] = 1
    for row in range(n):
        for col in range(n):
            if(zones[row][col]<= waterlevel):
                water_zone[row][col] = 0
    
    cnt = countZones(n,waterlevel)

    max_cnt = max(cnt, max_cnt)

print(max_cnt)
