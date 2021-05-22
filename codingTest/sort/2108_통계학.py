import sys
input = sys.stdin.readline
import math
from collections import defaultdict


def find_sum(numbers):
    return round(sum(numbers)/len(numbers))

def find_range(numbers):
    return numbers[-1] - numbers[0]

def find_mode(numbers):
    counter = defaultdict(int)
    
    for number in numbers:
        counter[number] += 1
    
    sorted_counter = sorted(counter.items(), key=lambda x: x[1], reverse = True)

    i = 0
    max1 = 0
    for counts in sorted_counter:
        if i == 0:
            max1 = counts[1]
            mode = counts[0]
            i += 1
        else:
            if max1 == counts[1]:
                mode = counts[0]
            break
    
    return mode

def find_mid(numbers):
    return numbers[len(numbers)//2]


n = int(input())
numbers = [int(input()) for _ in range(n)]
numbers.sort()

# 산술평균
print(find_sum(numbers))
# 중앙값
print(find_mid(numbers))
# 최빈값
print(find_mode(numbers))
# 범위
print(find_range(numbers))