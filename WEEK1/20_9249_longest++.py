import sys  
arr1 = str(sys.stdin.readline().split())
arr2 = sys.stdin.readline().split()

print(type(arr1))
print(len(arr1))
print(len(arr2))

print(arr2 in arr1)