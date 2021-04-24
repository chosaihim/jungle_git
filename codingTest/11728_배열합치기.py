import sys
input = sys.stdin.readline

n, m = list(map(int, input().split()))
a = list(map(int, input().split()))
b = list(map(int, input().split()))

union_set = set(a)|set(b)
union_list = list(union_set)
union_list.sort()

print(union_list)

for element in union_list:
    print(element ,end=' ')
