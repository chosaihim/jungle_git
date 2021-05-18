import sys
input = sys.stdin.readline
from collections import deque

from itertools import combinations
from itertools import permutations


sys.setrecursionlimit(10**6)


#
import heapq
# heapq 모듈은 이진 트리(binary tree) 기반의 최소 힙(min heap)
heap = []
heapq.heappush(heap, 50)
heapq.heappush(heap, 10)
heapq.heappush(heap, 20)
heap2 = [50 ,10, 20]
heapq.heapify(heap2)
result = heapq.heappop(heap)