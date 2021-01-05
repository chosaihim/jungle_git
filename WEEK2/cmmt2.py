# 막대끼리 닿은 경우 => 생기는 막대개수 : 0
# 막대개수:
import sys

sys.stdin = open('02.txt')


str = input()
str = list(str)
N = len(str)
stk = []
lstk = []
summ = 0

for i in range(N):
    l = len(stk)
    if '(' == str[i]:
        stk.append(1)
        lstk.append('(')
    elif l > 0:

        if ')' == str[i]:

            stk.pop()
            lstk.pop()
            # stk.append(0)
            if '(' != str[i-1]:
                summ += 1

            # l -= 1

            if len(lstk) != 0 and stk[-1] == 0:
                summ += 1*len(lstk)
            summ += sum(stk)

            while len(stk) != 0:# and stk[-1] > 0
                stk.pop()

            stk.append(summ)
            summ = 0
    else:
        print(0)
        exit(0)
else:
    print(sum(stk))