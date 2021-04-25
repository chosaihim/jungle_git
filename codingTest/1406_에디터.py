import sys
input = sys.stdin.readline

n = input()
m = int(input())

print(f'\nn:{n}, m:{m}')

str_len = len(n)-1
print(str_len)
cursor = str_len

print("\n--------")
print(f'n:{n}')
for i in range(m):
    instruction = input()
    print(f'instruction: {instruction}')
    if instruction[0] == 'L':
        cursor -= 1
        if cursor < 0: cursor = 0
        print("cursor: ", cursor)
    elif instruction[0] == 'D':
        cursor += 1
        if cursor == str_len: cursor = str_len-1
        print("cursor: ", cursor)
    elif instruction[0] == 'B':
        if cursor != 0:
            cursor -= 1
            n.remove(cursor)
            str_len -= 1
        print("cursor: ", cursor)
    elif instruction[0] == 'P':
        print(instruction[2])
        n = n[0:cursor] + instruction[2] + n[cursor:str_len]
        str_len += 1
        cursor += 1
        print("cursor: ", cursor)

    print(f'n:{n}')
    print("\n--------")
        
print(n)

# L	커서를 왼쪽으로 한 칸 옮김 (커서가 문장의 맨 앞이면 무시됨)
# D	커서를 오른쪽으로 한 칸 옮김 (커서가 문장의 맨 뒤이면 무시됨)
# B	커서 왼쪽에 있는 문자를 삭제함 (커서가 문장의 맨 앞이면 무시됨)
# 삭제로 인해 커서는 한 칸 왼쪽으로 이동한 것처럼 나타나지만, 실제로 커서의 오른쪽에 있던 문자는 그대로임
# P $	$라는 문자를 커서 왼쪽에 추가함