import sys
sys.setrecursionlimit(10**8) # 10^8 까지 늘림.



# FUNCTIONS ###########################################
def isSafe(n,x,y,waterlevel):
    if(0<=x<n and 0<=y<n):
        if(water_zone[x][y] == 1):      #지금 들어온 구역이 안전구역이면 검사 시작!
            water_zone[x][y] = 2        #water zone에 해당 구역 체크
            isSafe(n, x  ,y-1,waterlevel)   # 위쪽
            isSafe(n, x-1,y  ,waterlevel)   # 왼쪽
            isSafe(n, x+1,y  ,waterlevel)   # 오른쪽
            isSafe(n, x  ,y+1,waterlevel)   # 아래 로 검사구역 확장! 
            return None
        else:
            return None

# nxn행렬에서 수위가 waterlevel일 때, safezone이 몇개인지 세는 함수
def countZones(n,waterlevel):
    zone_cnt = 0
    for y in range(n):                      # 한 줄 씩 아래로 내려가면서
        for x in range(n):                  # 한 칸 씩 옆으로 이동해가면서
            if(water_zone[x][y] == 1):      # 물에 잠겨있지 않으면(1) 여기서부터 safezone 검사
                isSafe(n,x,y,waterlevel)
                zone_cnt += 1               # isSafe 빠져나오면 safezone 카운트 추가!
            else: continue
    return zone_cnt
###########################################################


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
for waterlevel in range(max_zone+1):

    #water_zone 만들기 (물에 잠긴 지역 표시: 0잠김 1안전)    
    for row in range(n):
        for col in range(n):
            water_zone[row][col] = 1
    for row in range(n):
        for col in range(n):
            if(zones[row][col]<= waterlevel):
                water_zone[row][col] = 0
    
    cnt = countZones(n,waterlevel)  # 각 수위마다 안전지역 개수
    
    # print(waterlevel, ", cnt: ", cnt)
    max_cnt = max(cnt, max_cnt)     # 최대 안전지역 개수와 비교하여 더 크면 갈아끼우기!

print(max_cnt)
