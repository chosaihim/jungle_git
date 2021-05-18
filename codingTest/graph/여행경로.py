def solution(tickets):
    import copy
    answer = []
    
    len_ticket = len(tickets)
    
    dic ={}
    dic['start'] = ['ICN']
    for depature, arrival in tickets:
        if dic.get(depature):
            dic[depature].append(arrival)
        else:
            dic[depature] = [arrival]
    
    routes[t[0]] = routes.get(t[0], []) + [t[1]]

    # print(dic)
    
    temp_answer = []
    
    def dfs(depature, arrival):
        print(f'-here:{arrival} from:{depature}-')
        
        len_ticket = len(tickets)
        temp_answer.append(arrival)
        if len(temp_answer) == len_ticket+1:
            temp = copy.deepcopy(temp_answer)
            answer.append(temp)
            # print(temp)
        
        
        # print(dic)
        if dic.get(arrival):
            
                new_arrival = dic[arrival].pop()
                dfs(arrival,new_arrival)
        
        # print(dic)
        
        dic[depature].append(arrival)
        temp_answer.pop()
        
    
    dfs('start', 'ICN')
    print(answer)
    
    return answer

tickets = [["ICN", "SFO"], ["ICN", "ATL"], ["SFO", "ATL"], ["ATL", "ICN"], ["ATL","SFO"]]
#return ["ICN", "ATL", "ICN", "SFO", "ATL", "SFO"]
solution(tickets)

from collections import defaultdict


def solution(tickets):
    answer = []
    adj = defaultdict(list)

    for ticket in tickets:
        adj[ticket[0]].append(ticket[1])

    for key in adj.keys():
        adj[key].sort(reverse=True)

    q = ['ICN']
    while q:
        tmp = q[-1]

        if not adj[tmp]:
            answer.append(q.pop())
        else:
            q.append(adj[tmp].pop())
    answer.reverse()
    return answer