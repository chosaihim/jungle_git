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
    if sum_combination == m:
        answer = m
        break
    
        
print(answer)
    