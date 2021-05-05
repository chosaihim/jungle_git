#436ms
import sys
input = sys.stdin.readline

n = int(input())
scores = []

for i in range(n):
    score_str = input().split()
    scores.append([str(score_str[0]), int(score_str[1]), int(score_str[2]), int(score_str[3])])

sorted_scores = sorted(scores, key = lambda x:(-x[1], x[2], -x[3], x[0]))

for person in sorted_scores: print(person[0])

# #360ms
# import sys
# n = int(sys.stdin.readline().rstrip())
# student=[]
# for _ in range(n):
#     g = list(sys.stdin.readline().rstrip().split())
#     student.append((100-int(g[1]),int(g[2]),100-int(g[3]),g[0]))

    
# student.sort()
# for st in student: print(st[3])

