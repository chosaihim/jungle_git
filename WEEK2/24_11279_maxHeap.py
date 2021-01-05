import sys
from typing import MutableSequence


def down_heap(a: MutableSequence, left: int, right: int) -> None:
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


def heap_push(a, in_int):
    a.append(in_int)
    last = len(a)-1      #마지막 원소
    
    while last > 0:

        parent = (last-1) //2  
        if a[parent] > a[last] : break

        a[last] = a[parent]
        last = parent    
        a[last] = in_int
    
    print(a)

def heap_pop(a):
    print(a[0])

    if(len(a) > 1 ): 
        a[0] = a[-1]
        a.pop()
        down_heap(a,0,len(a)-1)
    elif len(a) == 1:
        a.pop()



n = list(map(int, sys.stdin.readline().split()))[0]
a = []
for _ in range(n):
    cmd = list(map(int, sys.stdin.readline().split()))[0]

    if cmd == 0:
        # pop
        if len(a) == 0: print(0);
        else: 
            heap_pop(a)
            None
    else:
        #Push
        heap_push(a, cmd)
        None
