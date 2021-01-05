import sys
from heapq import heappop, heappush, heapify
input = sys.stdin.readline
N, idx = map(int, input().split())
nums = list(map(int, input().split()))

heap = nums[:]
count = 0

while count < idx:
    a = heappop(heap)
    for num in nums:
        if a*num not in heap:
            heappush(heap, a*num)
    count += 1

print(a)