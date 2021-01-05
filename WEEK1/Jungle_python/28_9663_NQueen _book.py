import sys, math
n = int((sys.stdin.readline().split())[0])

# [Do it! 실습 5-9] 8퀸 문제 알고리즘 구현하기

cnt = 0
pos = [0] * n          # 각 열에 배치한 퀸의 위치
flag_a = [False] * n   # 각 행에 퀸을 배치했는지 체크
flag_b = [False] * n*2  # 대각선 방향(↙↗)으로 퀸을 배치했는지 체크
flag_c = [False] * n*2  # 대각선 방향( ↘↖)으로 퀸을 배치했는지 체크

def put() -> None:
    """각 열에 배치한 퀸의 위치를 출력"""
    for i in range(n):
        print(f'{pos[i]:2}', end='')
    print()

def set(i: int) -> None:
    global n
    global cnt
    """i 열의 알맞은 위치에 퀸을 배치"""
    for j in range(n):
        if(     not flag_a[j]            # j행에 퀸이 배치 되지 않았다면
            and not flag_b[i + j]        # 대각선 방향(↙↗)으로 퀸이 배치 되지 않았다면
            and not flag_c[i - j + n-1]):  # 대각선 방향( ↘↖)으로 퀸이 배치 되지 않았다면
            pos[i] = j  # 퀸을 j행에 배치
            if i == n-1:  # 모든 열에 퀸을 배치하는 것을 완료
                # put()
                cnt += 1
            else:
                flag_a[j] = flag_b[i + j] = flag_c[i - j + n-1] = True
                set(i + 1)  # 다음 열에 퀸을 배치
                flag_a[j] = flag_b[i + j] = flag_c[i - j + n-1] = False

set(0)  # 0열에 퀸을 배치
print(cnt)