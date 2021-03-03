# https://programmers.co.kr/learn/courses/30/lessons/12899#

def solution(n):
    answer = ''
    
    while(n != 0):
        n -= 1
        digit = n % 3
        n = n//3
        
        if digit == 2:
            answer = str(4) + answer
        else:        
            answer = str(digit+1) + answer
    
    return answer

print(solution(10))

# 다른 사람 풀이
def change124(n):
    num = ['1','2','4']
    answer = ""


    while n > 0:
        n -= 1
        answer = num[n % 3] + answer
        n //= 3

    return answer