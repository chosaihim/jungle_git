import sys
input = sys.stdin.readline

#input
T = int(input())

for testcase in range(T):
    n = int(input())
    scores = [list(map(int,input().split())) for _ in range(n)]

    scores.sort()

    second_subject_top = scores[0][1]
    newbie_cnt = n

    for score in scores:
        if second_subject_top < score[1]: newbie_cnt -= 1
        elif second_subject_top > score[1]: second_subject_top = score[1]
           
    print(newbie_cnt)
