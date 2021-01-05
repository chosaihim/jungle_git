import sys
from typing import MutableSequence

def down_minheap(a: MutableSequence, left: int, right: int) -> None:
    temp = a[left]      # 루트

    parent = left
    while parent < (right + 1) // 2:
        cl = parent * 2 + 1     # 왼쪽 자식
        cr = cl + 1             # 오른쪽 자식
        child = cr if cr <= right and a[cr] < a[cl] else cl  # 큰 값을 선택합니다.
        if temp <= a[child]:
            break
        a[parent] = a[child]
        parent = child
    a[parent] = temp

def minheap_pop(a):
    # print(a[0])
    ret = a[0]

    if(len(a) > 1 ): 
        a[0] = a[-1]
        a.pop()
        down_minheap(a,0,len(a)-1)
    elif len(a) == 1:
        a.pop()
    
    # print(a)
    return ret

def minheap_push(a, in_int):
    a.append(in_int)
    last = len(a)-1      #마지막 원소
    
    while last > 0:

        parent = (last-1) //2  
        if a[parent] < a[last] : break

        a[last] = a[parent]
        last = parent    
        a[last] = in_int


def down_maxheap(a: MutableSequence, left: int, right: int) -> None:
    temp = a[left]      # 루트

    parent = left
    while parent < (right + 1) // 2:
        cl = parent * 2 + 1     # 왼쪽 자식
        cr = cl + 1             # 오른쪽 자식
        child = cr if cr <= right and a[cr] > a[cl] else cl  # 큰 값을 선택합니다.
        if temp >= a[child]:
            break
        a[parent] = a[child]
        parent = child
    a[parent] = temp

def maxheap_pop(a):
    # print(a[0])
    ret = a[0]

    if(len(a) > 1 ): 
        a[0] = a[-1]
        a.pop()
        down_maxheap(a,0,len(a)-1)
    elif len(a) == 1:
        a.pop()
    
    # print(a)
    return ret
        
def maxheap_push(a, in_int):
    a.append(in_int)
    last = len(a)-1      #마지막 원소
    
    while last > 0:

        parent = (last-1) //2  
        if a[parent] > a[last] : break

        a[last] = a[parent]
        last = parent    
        a[last] = in_int


maxheap = []
minheap = []
cur_mid = 0
n = list(map(int, sys.stdin.readline().split()))[0]
for _ in range(n):
    new = list(map(int, sys.stdin.readline().split()))[0]

    # print(f'current mid: {cur_mid}')

    #일단 힙에 넣고
    if(len(maxheap) == len(minheap) == 0):
        cur_mid = new
        maxheap_push(maxheap,new)
    else:
        if(new < cur_mid):
            maxheap_push(maxheap,new)
        else:
            minheap_push(minheap,new)
    
    
    # print(f'1 max{maxheap} << {cur_mid} << min{minheap}')
    if(len(minheap)>len(maxheap)):
        if(len(minheap)>len(maxheap)+1):
            # print('pop from min heap')
            temp = minheap_pop(minheap)
            # print(f'temp:{temp}')
            maxheap_push(maxheap,temp)
        cur_mid = minheap[0]
    else:
        if(len(maxheap)>len(minheap)+1):
            # print('pop from max heap')
            temp = maxheap_pop(maxheap)
            minheap_push(minheap,temp)
        cur_mid = maxheap[0]

    if(len(minheap) == len(maxheap)):
        cur_mid = maxheap[0]


    # print("max:", maxheap)
    # print("min:", minheap)
    # print(cur_mid)
    
    # print(f'max{maxheap} << {cur_mid} << min{minheap}')
    print(cur_mid)

