import sys
input = sys.stdin.readline

#input
n = int(input())
meetings = [list(map(int,input().split())) for _ in range(n)]

meetings.sort(key=lambda x:x[1])  
meetings.sort()
# print(meetings)

meeting = []
meeting.append(meetings[0])
m_begin = meetings[0][0]
for meet in meetings[1:]:
    if m_begin < meet[0]:
        meeting.append(meet)
        m_begin = meet[0]

# print(meeting)


# max_cnt = 0
# for start in range(len(meeting)):
#     cnt = 1
#     begin = start
#     for next_ in range(start+1,len(meeting)):
#         # print(f'begin:{meeting[begin]}, next_:{meeting[next_]}, cnt:{cnt}')
#         # if (meetings[begin][0] < meetings[next_][0]):
#         if (meeting[begin][1] <= meeting[next_][0]):
#             begin = next_
#             # print(f'now begin is {begin}')
#             cnt += 1
        
#         max_cnt = max(max_cnt, cnt)

cnt = 1
begin = 0
end = meeting[0][1]
for nextMeeting in range(1, len(meeting)):
    # print(f'begin:{begin}, end:{end}, nextMeeting:{meeting[nextMeeting]} cnt:{cnt}')

    if end > meeting[nextMeeting][1]:
        begin = meeting[nextMeeting][0]
        end = meeting[nextMeeting][1]
    
    elif end <= meeting[nextMeeting][0]:
        begin = meeting[nextMeeting][0]
        end = meeting[nextMeeting][1]
        cnt += 1

print(cnt)
        
    
    
    


# print(max_cnt)

# DP로 풀수 있나?