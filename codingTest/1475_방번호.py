# 72ms
# import sys
# input = sys.stdin.readline

# roomNumber = list(map(int, list(input().strip())))
# left_numbers = [1] * 10
# set_count = 1

# for number in roomNumber:
#     if left_numbers[number] > 0:
#         left_numbers[number] -= 1
#     else:
#         if number == 6 and left_numbers[9] > 0:
#             left_numbers[9] -= 1
#         elif number == 9 and left_numbers[6] > 0:
#             left_numbers[6] -= 1
#         else:
#             set_count += 1
#             for i in range(10):
#                 left_numbers[i] += 1
#             left_numbers[number] -= 1

# print(set_count)

#52ms
# n = input()
# count = 0
# cards = []
# for ch in n:
#     if ch == '9': ch = '6'
#     if ch not in cards:
#         tmp = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '6']
#         tmp.remove(ch)
#         cards.extend(tmp)
#         count += 1
#     else:
#         cards.remove(ch)

# print(count)

import sys
input = sys.stdin.readline

roomNumber = input().strip()
set_count = 1
card_set = ['0','1','2','3','4','5','6','7','8','6']

for number in roomNumber:
    if number == '9': number = '6'
    
    if number in card_set:
        card_set.remove(number)
    else:
        card_set += ['0','1','2','3','4','5','6','7','8','6']
        set_count += 1
        card_set.remove(number)

print(set_count)