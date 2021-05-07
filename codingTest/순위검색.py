import sys
import copy
import re
input = sys.stdin.readline

def solution(info, query):
    answer = []
    
    info_table = []
    for data in info:
        info_table.append(list(map(str,data.split())))
    
    queries = []
    for que in query:
        que = re.sub("and", "", que)
        queries.append(list(map(str,que.split())))    
    
    for que in queries:
        table = []

        for t in info_table:
            if int(que[-1]) <= int(t[-1]):
                table.append(t)
        left_table = table
        
        for i in range(len(que)-1):
            if que[i] == "-": continue
            left_table = []
            for t in table:
                if que[i] == t[i]:
                    left_table.append(t)
            table = left_table
        
        answer.append(len(left_table))
    
    return answer


info = ["java backend junior pizza 150","python frontend senior chicken 210","python frontend senior chicken 150","cpp backend senior pizza 260","java backend junior chicken 80","python backend senior chicken 50"]
query = ["java and backend and junior and pizza 100","python and frontend and senior and chicken 200","cpp and - and senior and pizza 250","- and backend and senior and - 150","- and - and - and chicken 100","- and - and - and - 150"]
# answer = [1,1,1,1,2,4]
print(solution(info, query))