import sys
from collections import deque
input = sys.stdin.readline
import math

# 소수 판별 함수(에라토스테네스의 체)
def getPrimeTable(n):
    # 2부터 n까지의 모든 수에 대하여 소수 판별
    array = [1 for i in range(n+1)] # 처음엔 모든 수가 소수(True)인 것으로 초기화(0과 1은 제외)

    # 에라토스테네스의 체
    for i in range(2, int(math.sqrt(n)) + 1): #2부터 n의 제곱근까지의 모든 수를 확인하며
        if array[i] == 1: # i가 소수인 경우(남은 수인 경우)
            # i를 제외한 i의 모든 배수를 지우기
            j = 2
            while i * j <= n:
                array[i * j] = 0
                j += 1
    return array
    # return [ i for i in range(2, n+1) if array[i] ]

# N이 1,000,000 이내로 주어지는 경우 활용할 것 => 이론상 400만번 정도 연산이고 메모리도 충분함



def bfs(start, goal):
    visited[start] = 1
    depth = 0
    root = [start, 0]
    queue = deque([root])
    
    
    while queue:
        # print(queue)
        num, depth = queue.popleft()
        
        if num == goal: return depth
        
        for pos in range(0,4):
            for i in range(0,10):
                tmp = int(str(num)[:pos] + str(i) + str(num)[pos+1:])
                
                if tmp > 1000 and visited[tmp] == 0 and prime_table[tmp]:
                    queue.append([tmp,depth+1])
                    visited[tmp] = 1
        
    



prime_table = getPrimeTable(10000)
#### INPUT ####
T = int(input())

for t in range(T):
    start, goal = map(int, input().split())
    visited = [0] * 10000
    print(bfs(start,goal))
    
    