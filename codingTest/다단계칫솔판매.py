import sys

def solution(enroll, referral, seller, amount):
    answer = []
    graph = {}
    money = {}
    
    # 배정
    for e, r in zip(enroll,referral):
        graph[e] = r
        money[e] = 0
    
    # 돈 배분 함수
    def share(person, earn):
        if(earn < 10):
            money[person] += earn
        else:
            fee =  earn//10
            money[person] += (earn-fee)
            if(graph[person] != "-"):
                share(graph[person], fee)
    
    # 배분
    for s, a in zip(seller, amount):
        share(s,a*100)
    
    # 답
    for person in enroll:
        answer.append(money[person])
        
    
    return answer






enroll = ["john", "mary", "edward", "sam", "emily", "jaimie", "tod", "young"]
referral = ["-", "-", "mary", "edward", "mary", "mary", "jaimie", "edward"]
seller = ["young", "john", "tod", "emily", "mary"]
amount = [12, 4, 2, 5, 10]
result = [360, 958, 108, 0, 450, 18, 180, 1080]

print(solution(enroll,referral,seller,amount))