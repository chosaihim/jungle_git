import sys
input = sys.stdin.readline

n = list(map(int, sys.stdin.readline().split()))
a = list(map(int, sys.stdin.readline().split()))
b = list(map(int, sys.stdin.readline().split()))

a_set = set(a)
b_set = set(b)

print(len(a_set-b_set)+len(b_set-a_set))

## 참고코드
# input()
# a = list(input().split())
# b = list(input().split())
# print(2*len(set(a+b)) - (len(a)+len(b)))