import sys
input = sys.stdin.readline

#input
n = int(input())
meetings = [list(map(int,input().split())) for _ in range(n)]

# meetings.sort(key=lambda x:x[1])  
meetings.sort()

cnt = 1
begin = 0; end= 10**10

for nextMeeting in meetings:
    next_begin, next_end = map(int, nextMeeting)

    if end > next_end:      #현재 회의보다 같이 혹은 늦게 시작하고 먼저 끝나는 회의가 있다면 현재회의를 그 회의로 교체
        # begin = next_begin
        end   = next_end
    
    elif end <= next_begin: #현 회의가 끝나고 다음 회의가 시작하면 cnt 올려주고 현재회의를 다음회의로 교체
        # begin = next_begin
        end   = next_end
        cnt += 1

print(cnt)

# DP로 풀수 있나?