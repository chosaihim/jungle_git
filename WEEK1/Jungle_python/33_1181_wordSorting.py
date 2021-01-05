import sys
n = int((sys.stdin.readline().split())[0])

arr_in = []

for i in range(n):
    arr_in.append(str((sys.stdin.readline().split())[0]))

arr_in = list(set(arr_in))
arr_in.sort()
arr_in.sort(key=len)
    
for i in range(len(arr_in)):
    print(arr_in[i])
