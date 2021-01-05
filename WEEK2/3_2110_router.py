import sys
debugFlag = False

### FUNCTION
def router(h_locations:list, num_router:int):
    if(debugFlag): print(f'num of router:{num_router}')

    pl = 1                      # 거리의 최소값은 0이 될 수 없어서 lowest 값이 1 !!!!! 이게 0이어서 계속 오답이었음!!!
    pr = h_locations[-1] - h_locations[0]  # 검색 범위의 맨 끝 원소의 인덱스
    ok_dist = 0

    while True:
        pc = (pl+pr)//2
        if(debugFlag): print(f'minimum distance:{pc}')
        
        if pc == 0: break

        if IsPossibleSetAll(h_locations,pc) >= num_router:
            pl = pc+1
            ok_dist = max(pc,ok_dist)            
            if(debugFlag): print(f'try longer min, ok_disk = {ok_dist}')
        else:               
            if(debugFlag): print(f'try shorter min')
            pr = pc-1      # 검색 범위를 앞쪽 절반으로
        
        if pl > pr:
            break


    return ok_dist

def IsPossibleSetAll(h_locations:list, min_dist:int):
    # 최소거리와 집들의 위치 정보, 라우터의 개수가 주어졌을 때 
    # 최소거리 이상으로 라우터를 설치하면 라우터를 모두 설치할 수 있는지 검사
    
    last_router = h_locations[0]
    set_router = 1   # 가장 앞집에 라우터 설치
    
    for h in range(1,len(h_locations)):
        if(debugFlag): print(f'---distance from previous router:{h_locations[h]-last_router}')
        if(h_locations[h]-last_router) >= min_dist:
            if(debugFlag): print(f'>>>set Router at {h_locations[h]}')
            set_router += 1
            last_router = h_locations[h]
    
    if(debugFlag): print(f'set routers: {set_router}')
    return set_router


#### MAIN ####
# input 받아오는 부분
n_house, n_router = list(map(int, sys.stdin.readline().split()))

locations = []
locations.append(list(map(int, sys.stdin.readline().split()))[0])

for i in range(1,n_house):
    locations.append(list(map(int, sys.stdin.readline().split()))[0])
locations.sort()

print(router(locations, n_router))
