# https://www.acmicpc.net/problem/2643
#72ms
import sys
input = sys.stdin.readline

n = int(input())
paper = [list(map(int,input().split())) for _ in range(n)]

for i in range(n): paper[i].sort(reverse=True)
paper = sorted(paper, key = lambda x : (-x[0], -x[1]))

dp = [1] * n
for i in range(1,n):
    max_index = -1
    for j in range(i):
        if paper[j][0] >= paper[i][0] and paper[j][1] >= paper[i][1]:
            dp[i] = max(dp[i], dp[j]+1)

print(max(dp))
    
# #56ms
# import sys; s = sys.stdin.readline

# def pile(i):
#     if count[i]:
#         return count[i]
#     count[i] = 1
#     for j in range(len(colors)):
#         if i != j and colors[i][1] >= colors[j][1] and colors[i][0] >= colors[j][0]:
#             count[i] = max(count[i], pile(j)+1)
#     return count[i]



    
# colors = [sorted(list(map(int, s().split()))) for _ in range(int(s()))]
# count = [False] * len(colors)
# for i in range(len(colors)):
#     count[i] = pile(i)
# print(max(count))
