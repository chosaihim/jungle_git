import sys

arr = []
for i in range(9):
    arr.append(list(map(int, sys.stdin.readline().split()))[0])

print(max(arr))
print(arr.index(max(arr))+1)

