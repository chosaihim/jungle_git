import sys
input = sys.stdin.readline

n = int(input())
matrices = [list(map(int, input().split())) for _ in range(n)]
# cache = [[0 for _ in range(501)] for _ in range(501)]
cache = [[0 for _ in range(n)] for _ in range(n)]


# input: 시작점, 끝점 output: 1. 최소 계산 횟수 2.matrix 행 3. matrix 열
def multiply(start, end):

    min_multi = 10**10

    # 기저 조건
    if start == end: return 0, matrices[start][0], matrices[start][1]
    if (end - start) == 1: cache[start][end] = matrices[start][0] * matrices[start][1] *matrices[end][1]; return matrices[start][0] * matrices[start][1] *matrices[end][1], matrices[start][0], matrices[end][1]
    
    # 아는 값
    if cache[start][end]: return cache[start][end], matrices[start][0], matrices[end][1]
    # 모르는 값
    if start < end:
        for mid in range(start, end):
            result1 = multiply(start,mid)[0]
            if(result1 > min_multi): continue   # 시간을 줄여보려는 몸부림
            
            result_mid = matrices[start][0] * matrices[mid][1] * matrices[end][1]
            if result_mid > min_multi: continue

            result2 = multiply(mid+1,end)[0]
            if(result2 > min_multi): continue
            
            result = result1 + result_mid + result2

            if(result < min_multi):
                min_multi = result
    
    cache[start][end] = min_multi
    return min_multi, matrices[start][0], matrices[end][1]

print(multiply(0,n-1)[0])