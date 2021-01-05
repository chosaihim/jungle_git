import sys
n = int((sys.stdin.readline().split())[0])

arr_in = []

for i in range(n):
    arr_in.append(int((sys.stdin.readline().split())[0]))

arr_in.sort()

for i in range(n):
    print(arr_in[i])