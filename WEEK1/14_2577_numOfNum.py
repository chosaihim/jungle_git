import sys  
a = list(map(int, sys.stdin.readline().split()))[0]
b = list(map(int, sys.stdin.readline().split()))[0]
c = list(map(int, sys.stdin.readline().split()))[0]

product = a * b * c

digits = list(map(int,str(product)))

print(digits)
    
for i in range(10):
    print(digits.count(i))