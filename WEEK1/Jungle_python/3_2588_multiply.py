a = int(input())
b = int(input())

l = []

for i in map(int, str(b)):
    l.append(a*i)

for i in reversed(l):
    print(i)

print(a*b)
