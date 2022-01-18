import sys

#시간초과
# def solution(stones, k):
#     answer = 0
#     if k == 1:
#         if min(stones) == 0:
#             answer = 0
#         else:
#             answer = max(stones)
#     else:    
#         for i in range(k,len(stones)):
#             stones[i] = min(stones[i], max(stones[i-k:i-1]))
#         answer = max(stones[i-k:i-1])
#     return answer

def solution(stones, k):
    answer = 0
    
    left = 0; right = max(stones)
    
    while True:
        mid = (left + right) // 2
        
        if(crossBridge(mid, stones, k)):
            answer = max(answer,mid)
            left = mid + 1
        else:
            right = mid - 1
        
        if left > right:
            break
        
    return answer


def crossBridge(num, stones, k):
    blank = 0
    for s in stones:
        # 연속적으로 사람수보다 작은 수의 돌이 나오면 징검다리 못 건넘
        if s < num:
            blank += 1
            if blank == k:
                return False
        else:
            blank = 0
    return True

stones = [2, 4, 5, 3, 2, 1, 4, 2, 5, 1]
k = 3
# result = 3
print(solution(stones, k))