import sys
from itertools import permutations
import re
input = sys.stdin.readline

operator = ['+','-','*']
priorities = list(permutations(operator))
# print(priorities)

def solution(expression):
    answer = 0
    total = 0
    
    # 수식 숫자 구분하기
    numbers = list(map(int, re.findall("\d+", expression)))
    operators = re.findall("['+','\-','*']", expression)    
    
    for priority in priorities: # 순열 중에 하나 선택
        n = numbers
        o = operators
        temp_n = []
        temp_o = []
        for operator in priority: # 연산자 하나 선택
            left = n[0]
            for i in range(len(o)):
                if o[i] != operator:
                    temp_n.append(left)
                    left = n[i+1]
                    temp_o.append(o[i])
                    if i == len(o) - 1:
                        temp_n.append(left)
                else:
                    if operator == "+":
                        left = left + n[i+1]
                    elif operator == "*":
                        left = left * n[i+1]
                    else:
                        left = left - n[i+1]
                        
                    if i+1 == len(o):
                        temp_n.append(left)
            
            n = temp_n
            o = temp_o
            temp_n = []
            temp_o = []
    
        answer = max(answer, abs(left))
    return answer




expression = "100-200*300-500+20"
# result = 60420
print(solution(expression))