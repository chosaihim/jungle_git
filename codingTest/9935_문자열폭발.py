# https://www.acmicpc.net/problem/9935

import sys
input = sys.stdin.readline
from collections import deque

#input from testcase
input_str = list(input().strip())
bomb = input().strip()

bomb_len = len(bomb)
answer = deque()


def compareString(answer, bomb):
    for i in range(len(bomb)):
        if answer[len(answer)-(len(bomb))+i] != bomb[i]:
            return False
    return True       
    

for next_char in input_str:
    answer.append(next_char)
    if next_char == bomb[-1] and len(answer) >= bomb_len:
        if compareString(answer, bomb):
            for i in range(bomb_len):
                answer.pop()
    
print("".join(answer)) if answer else print("FRULA")


# 시간초과
# in_str = in_str.replace(bomb,"")
# prev_str_len = 0
# while (prev_str_len != len(in_str)):
#     prev_str_len = len(in_str)
#     in_str = in_str.replace(bomb,"")
# print(in_str) if len(in_str)>0 else print("FRULA")