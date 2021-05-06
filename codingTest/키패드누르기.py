import sys
input = sys.stdin.readline

def solution(numbers, hand):
    answer = ''
    
    left = [3,0]
    right = [3,2]
    
    for number in numbers:
        if number == 1 or number == 4 or number == 7:
            answer += 'L'
            left = [(number//3),0]
        elif number == 3 or number == 6 or number == 9:
            answer += 'R'
            right = [(number-1)//3,2]
        else:
            if number == 0: key_pos = [3,1]
            else: key_pos = [(number//3),1]
            
            if abs(key_pos[0]-left[0]) + abs(key_pos[1]-left[1]) < abs(key_pos[0]-right[0]) + abs(key_pos[1]-right[1]):
                answer += 'L'
                left = key_pos
            elif abs(key_pos[0]-left[0]) + abs(key_pos[1]-left[1]) > abs(key_pos[0]-right[0]) + abs(key_pos[1]-right[1]):
                answer += 'R'
                right = key_pos
            else:
                if hand == "right": 
                    answer += 'R'
                    right = key_pos
                else:
                    answer += 'L'
                    left = key_pos
                
    return answer




numbers = [1, 3, 4, 5, 8, 2, 1, 4, 5, 9, 5]	
hand = "right"
#result = "LRLLLRLLRRL"

numbers = [7, 0, 8, 2, 8, 3, 1, 5, 7, 6, 2]
hand = "left"
#기댓값 〉	"LRLLRRLLLRR"
print(solution(numbers, hand))
