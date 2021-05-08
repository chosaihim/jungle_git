def solution(gems):
    answer = [0,0]
    
    gem_set = set(gems)
    len_set = len(gem_set)
    
    # 거의 다 되지만 시간 초과
    #해설읽고 다시 품
    # gem_map = {}
    # min_len = 1000001
    # for i in range(len(gems)):
    #     gem_map[gems[i]] = i
        
    #     if len(gem_map) == len(gem_set):
    #         values = list(gem_map.values())
    #         temp_len = max(values)-min(values)
            
    #         if min_len > temp_len:
    #             min_len = temp_len
    #             answer = [min(values)+1,max(values)+1]
        
    # 시간초과
    # min_len = 1000001
    # for start in range(len(gems)):
    #     for end in range(start + len_set,len(gems)+1):
    #         temp = gems[start:end]
    #         if len(set(temp)) == len_set:
    #             temp_len = end - start
    #             if temp_len == len_set:
    #                 answer = [start+1, end]
    #                 return answer
    #             if min_len > temp_len:
    #                 answer[0] = start + 1
    #                 answer[1] = end 
    #                 min_len = temp_len
    #             break
    
    return answer



# 다른 블로그에서 가져온 정답
# def solution(gems):
#     n = len(set(gems))
#     answer = [0, len(gems) - 1]
#     start = 0
#     end = 0
#     dic1 = {gems[0]: 1}
#     while start < len(gems) and end < len(gems):
#         if len(dic1) == n:
#             if answer[1] - answer[0] > end - start:
#                 answer[0] = start
#                 answer[1] = end
#             if dic1[gems[start]] == 1:
#                 del dic1[gems[start]]
#             else:
#                 dic1[gems[start]] -= 1
#             start += 1
#         else:
#             end += 1
#             if end == len(gems):
#                 break
#             else:
#                 if dic1.get(gems[end]) is None:
#                     dic1[gems[end]] = 1
#                 else:
#                     dic1[gems[end]] += 1
#     answer[0] += 1
#     answer[1] += 1
#     return answer