import sys
input = sys.stdin.readline
from itertools import combinations 

n, m = list(map(int, input().split())) # n: number of cards, m: goal number
cards = list(map(int, input().split())) # numbers on cards

card_combination = list(combinations(cards, 3))
answer = 0
for i in range(len(card_combination)):
    sum_combination = sum(card_combination[i])
    if sum_combination < m:
        answer = max(answer, sum_combination)
    elif sum_combination == m:
        answer = m
        break
    
        
print(answer)


## solution
# def GetMaxBlackJackNumbers(N, M, nums):
#     	sums = set()
# 	for i in range(N-2):
# 		for j in range(i+1, N-1):
# 			for k in range(j+1, N):
# 				sum = nums[i] + nums[j] + nums[k]
# 				if sum <= M:
# 					sums.add(sum)
# 					break

# 	return max([*sums])

# N, M = map(int, input().split())
# nums = sorted(list(map(int, input().split())), reverse=True)
# print(GetMaxBlackJackNumbers(N, M, nums))
    