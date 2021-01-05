import sys

cities = int((sys.stdin.readline().split())[0])

costs = []
for city in range(cities):
    cost = list(map(int, sys.stdin.readline().split()))
    costs.append(cost)

print(costs)


#route를 만들기 위해 visit이라는 2중 list 만들어 둠
# 방문할 수 있으면 true, 못하면 false
visits =[]
for i in range(cities):
    temp_visits = []
    for j in range(cities):
        if(costs[i][j] == 0): temp_visits.append(False)
        else: temp_visits.append(True)
    visits.append(temp_visits)


#find all possible routes
#start:start point, des:destination, rlen:route length, check: checklist  
def findroutes(stp,rlen,check):    
    rlen += 1
    routes = []
    temp_route =[]
    no_more = True
    rroute = []
    check_ori = check

    #현재 있는 도시는 다시 방문하지 않도록 check!(False)
    city_num = len(check[0])   
    if(stp != 0):                   # 첫번째 도시인 경우에는 나중에 돌아와야 하니 잠깐 예외처리
        for i in range(city_num):
            check[i][stp] = False
    
    
    #다음 도시로 이동!
    for goto in range(1,city_num):
        if(check[stp][goto]):       # visit가 true이면 방문!
            temp_route = (findroutes(goto,rlen,check))
            if(temp_route[0] == -1):
                routes.append(-1)
            else:
                routes.append(stp)
            no_more = False
        
        if(stp == 0):
            temp_route = [0] + temp_route
            rroute.append(temp_route)
            # print("rroute:", rroute)
            routes.clear()
    

        
    if(no_more):                    # 더 이상 방문할 수 있는 도시가 없으면 
        if(rlen == city_num):       # route의 길이를 검사            
            if(check[stp][0]):      # 마지막 도시에서 첫번쨰 도시로 갈 수 있으면 success & route 반환
                temp_route.append(stp)
            else:                   # 마지막 도시에서 첫번째 도시로 못가면 fail
                temp_route.append(-1)            
        else:                       # 전체를 못 돌면 fail 반환
            temp_route.append(-1)
    
    for i in range(len(temp_route)):
        routes.append(temp_route[i])

    routes= list(set(routes))
    
    # if(stp != 0):                   # 정상으로 돌려놓고 나가기
        # for i in range(city_num):
            # check[i][stp] = True
    if(stp != 0):
        check = check_ori
    
    if(stp == 0):
        return rroute
    else:
        return routes

print(findroutes(0,0,visits))