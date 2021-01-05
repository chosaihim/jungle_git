import sys
from typing import MutableSequence


def counting_sort(a: MutableSequence) :
    fsort(a, max(a))
    
def fsort(a: MutableSequence, max: int) :
    n = len(a)
    f = [0] * (max + 1)
    b = [0] * n
    
    for i in range(n) :             f[a[i]] += 1
    for i in range(1, max + 1) :    f[i] += f[i-1]
    for i in range(n - 1, -1, -1) : f[a[i]] -= 1; b[f[a[i]]] = a[i] #! 이 부분에서 앞에서 부터 스캔하면 안정적이지 않을 수 있다.
    for i in range(n) :             a[i] = b[i]
    
def counting_sorted(arr, K):
    c = [0] * K
    sorted_arr = [0] * len(arr)
    
    for i in arr:
        c[i] += 1
    
    for i in range(1,K):
        c[i] += c[i-1]
   
    for i in range(len(arr)):
        sorted_arr[c[arr[i]]-1] = arr[i]
        c[arr[i]] -= 1
    
    return sorted_arr
        

n = int((sys.stdin.readline().split())[0])

arr_in = []

for i in range(n):
    arr_in.append(int((sys.stdin.readline().split())[0]))

# print((arr_in))
arr_in = counting_sorted(arr_in,10000)
# print((arr_in))

# print(arr_in)
for i in range(n):
    print(arr_in[i])
