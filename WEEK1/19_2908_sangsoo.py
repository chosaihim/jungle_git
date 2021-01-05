import sys
a,b = list(map(str, sys.stdin.readline().split()))

a = a[::-1]
b = b[::-1]

print(max(int(a),int(b)))