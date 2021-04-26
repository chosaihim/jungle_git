import sys
input = sys.stdin.readline
from collections import deque

front_str = deque(list(input().strip()))
m = int(input())
back_str = deque()

# print(front_str)

for i in range(m):
    instruction = input()
    if instruction[0] == 'L':
        if front_str:
            back_str.append(front_str.pop())

    elif instruction[0] == 'D':
        if back_str:
            front_str.append(back_str.pop())

    elif instruction[0] == 'B':
        if front_str:
            front_str.pop()

    elif instruction[0] == 'P':
        front_str.append(instruction[2])


back_str = list(back_str)
print("".join(front_str) + "".join(back_str[::-1]))

# L	커서를 왼쪽으로 한 칸 옮김 (커서가 문장의 맨 앞이면 무시됨)
# D	커서를 오른쪽으로 한 칸 옮김 (커서가 문장의 맨 뒤이면 무시됨)
# B	커서 왼쪽에 있는 문자를 삭제함 (커서가 문장의 맨 앞이면 무시됨)
# 삭제로 인해 커서는 한 칸 왼쪽으로 이동한 것처럼 나타나지만, 실제로 커서의 오른쪽에 있던 문자는 그대로임
# P $	$라는 문자를 커서 왼쪽에 추가함