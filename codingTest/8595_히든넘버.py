import sys  
import re
input = sys.stdin.readline


def total_in_numbers(input_str):
    numbers = re.findall("\d+",input_str)
    total = 0
    for num in numbers:
        total += int(num)
    return total

input_len = input()
input_str = input()
print(total_in_numbers(input_str))


# num = '0'
# total = 0
# prev = 0

# for ch in input_str:
#     if ch.isdigit():
#         num += ch
#         prev = 1
#     elif prev:
#         total += int(num)
#         num = '0'
#         prev = 0
    
# print(total)
        