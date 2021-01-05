import sys

N = int(input())

paper =[]

for i in range(N):
    paper.append(input())
    paper[i] = list(paper[i])


def recur(x, y, n):
    global paper
    double_break = False
    num = paper[y][x]

    for m in range(y, y+n):

        if double_break:
            break

        for k in range(x, x+n):
            if paper[m][k] != str(num):
                print('(', end='')
                recur(x, y, n//2)
                recur(x + n//2, y, n//2)
                recur(x, y+n//2, n//2)
                recur(x + n//2, y + n//2, n//2)
                double_break = True     #이 영역은 다 돌았다!
                print(')', end='')
                break

    if not double_break:
        if int(num) == 1:
            print(1,end='')
            # print(str(x) + ' ' + str(y) + 'b')
        else:
            print(0,end='')
            # print(str(x) + ' ' + str(y) + 'w')


recur(0, 0, N)
