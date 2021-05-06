import sys
input = sys.stdin.readline

n, key = map(int, input().split())
numbers = list(map(int, input().split()))


def low_bound(a, key):
    pl = 0          # 검색 범위의 맨 앞 원소 인덱스
    pr = len(a) - 1 # 검색 범위의 맨 끝 원소의 인덱스

    while True:
        pc = (pl+pr)//2     #중앙 원소의 인덱스

        if a[pc] == key and a[pc-1] < key:    
            # return pc       #검색 성공
            return pc
        elif a[pc] < key:   
            pl = pc + 1     # 검색 범위를 뒤쪽 절반으로
        else:               
            pr = pc -1      # 검색 범위를 앞쪽 절반으로
        
        if pl > pr:
            break

        # return -1   # 검색실패
    return -1


def up_bound(a, key):
    pl = 0          # 검색 범위의 맨 앞 원소 인덱스
    pr = len(a) - 1 # 검색 범위의 맨 끝 원소의 인덱스

    while True:
        pc = (pl+pr)//2     #중앙 원소의 인덱스

        if a[pc] == key and a[pc+1] > key:    
            # return pc       #검색 성공
            return pc
        elif a[pc] <= key:   
            pl = pc + 1     # 검색 범위를 뒤쪽 절반으로
        else:               
            pr = pc -1      # 검색 범위를 앞쪽 절반으로
        
        if pl > pr:
            break

        # return -1   # 검색실패
    return -1

upper = up_bound(numbers, key)
if upper == -1: print(-1)
else:
    print(upper - low_bound(numbers, key) + 1)

# 7 2
# 1 1 2 2 2 2 3
# -> 4

# 7 4
# 1 1 2 2 2 2 3
# -> -1

import sys
from bisect import bisect_left, bisect_right

sys.stdin = open('input.txt')

N,M  = map(int, sys.stdin.readline().split())
array = list(map(int, sys.stdin.readline().split()))


startindex=bisect_left(array,M)
endindex=bisect_right(array,M)
print(endindex-startindex)