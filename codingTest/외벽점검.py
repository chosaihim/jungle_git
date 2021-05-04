# https://programmers.co.kr/learn/courses/30/lessons/60062?language=python3

def solution(n, weak, dist):
    answer = 0
    
    weak.sort()
    dist.sort(reverse = True)
    long_weak = weak + [ w+n for w in weak]
    weak_gap = [ weak[i] - weak[i-1] for i in range(1,len(weak))] + [weak[0]+ n - weak[-1]]
    
    print(long_weak)
    print(weak_gap)

    for start_index in range(len(weak)):
        weak_round = weak[start_index : start_index + len(weak)]
        dist_index = 0
        d = dist[dist_index]
        for i in range(1,len(weak_round)):
            if dist[dist_index] > weak_round[i] - weak_round[i-1]:
                break
            else:
                if d >= weak_round[i] - weak_round[i-1]:
                    d -= (weak_round[i] - weak_round[i-1])
            
    return answer

#input
n = 12; weak = [1, 5, 6, 10]; dist =[1, 2, 3, 4]	#2
# n = 12; weak = [1, 3, 4, 9, 10]; dist =[3, 5, 7]	#1
print(solution(n, weak, dist))



# #정답코드
# from itertools import permutations
# def solution(n, weak, dist):
#     # 1. 시계 / 반시계 문제 해결하기
#     weak_length = len(weak)
#     for i in range(weak_length):
#         weak.append(weak[i] + n)
#     # 4에서 반시계방향 = 9에서 시계방향. 
#     # 즉 길이를 두 배 늘려놓으면 굳이 방향 고민할 필요 없다
    
#     # 투입할 수 있는 친구의 최댓값. 
#     # 점검 불가능한 경우를 상정해서 len(dist) + 1
#     answer = len(dist) + 1
#     for i in range(weak_length):
        
#         # 2. 어디서부터 벽 점검을 시작할 것인지 결정
#         start_point = [weak[j] for j in range(i, i + weak_length)]
        
#         # 3. 벽 점검에 투입할 친구의 순서 정하기
#         candidates = permutations(dist, len(dist))
        
#         # 4. 탐색
#         for order in candidates:
#             # 순서대로 출발. 
#             friend_idx, friend_count = 0, 1
#             # 친구가 확인할 수 있는 최대 거리
#             possible_check_length = start_point[0] + order[friend_idx]
            
#             for idx in range(weak_length):
#                 # 확인할 수 있는 최대 거리를 넘어설 경우
#                 if start_point[idx] > possible_check_length:
#                     # 다음 친구 투입
#                     friend_count += 1
#                     # 더 이상 투입할 친구가 없는 경우 break
#                     if friend_count > len(order):
#                         break
#                     # 다음 친구 투입, 친구가 확인할 수 있는 최대 거리 업데이트
#                     friend_idx += 1
#                     possible_check_length = order[friend_idx] + start_point[idx]
#             # 투입할 친구 최솟값 업데이트                     
#             answer = min(answer, friend_count)
    
#     if answer > len(dist):
#         return -1
    
#     return answer