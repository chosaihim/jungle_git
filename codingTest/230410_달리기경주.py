# 프로그래머스
# https://school.programmers.co.kr/learn/courses/30/lessons/178871


# 시간초과.
# def solution(players, callings):
#     answer = players
    
#     for call in callings:
#         order = players.index(call)
#         players[order-1], players[order] = players[order], players[order-1]
        
#     return answer


def solution(players, callings):
    answer = []
    dic = {}
    dic_rank = {}

    for rank in range(len(players)):
        dic[players[rank]] = rank
        dic_rank[rank] = players[rank]

    for call in callings:
        r_now = dic[call]
        player = dic_rank[r_now]
        front = dic_rank[r_now-1]

        dic[player] = r_now-1
        dic[front] = r_now

        dic_rank[r_now-1] = player
        dic_rank[r_now] = front

    for i in range(len(players)):
        answer.append(dic_rank[i])


    return answer


players = ["mumu", "soe", "poe", "kai", "mine"]
callings = ["kai", "kai", "mine", "mine"]
solution(players, callings)