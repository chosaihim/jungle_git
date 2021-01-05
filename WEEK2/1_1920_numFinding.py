import sys
n      = list(map(int, sys.stdin.readline().split()))[0]
a_list = list(map(int, sys.stdin.readline().split()))
m      = list(map(int, sys.stdin.readline().split()))[0]
b_list = list(map(int, sys.stdin.readline().split()))

for b in b_list:
    if(b in a_list):
        print(1)
    else:
        print(0)