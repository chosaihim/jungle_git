import sys
input = sys.stdin.readline

n = int(input())
k = int(input())

# 이분탐색
def counting_less(n, x):
    
    count = 0
    for row in range(1, n+1):
        if row > x: break
        count += min(n, x//row)
    
    return count
        
    
def bin_search(n, key):
    pl = 1          # 검색 범위의 맨 앞 원소 인덱스
    pr = k          # 검색 범위의 맨 끝 원소의 인덱스
    answer = 1
    

    while True:
        pc = (pl+pr)//2     #중앙 원소의 인덱스

        if counting_less(n,pc) < key:   
            pl = pc + 1     # 검색 범위를 뒤쪽 절반으로
        else:
            answer = pc               
            pr = pc -1      # 검색 범위를 앞쪽 절반으로

        if pl > pr:
            break
        
    return answer

print(bin_search(n, k))
    

# 쌉시간초과
# Brute force
# heap = []
# for i in range(1,n+1):
#     for j in range(1, n+1):
#         heapq.heappush(heap, i*j)

# for _ in range(k-1):
#     heapq.heappop(heap)

# print(heapq.heappop(heap))
