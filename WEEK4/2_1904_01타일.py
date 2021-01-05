import sys
input = sys.stdin.readline

n = int(input())

# def binary(n):
    
#     if   n == 1: return 1 # 1
#     elif n == 2: return 2 # 00, 11

#     if cache[n]: return cache[n]
#     else:
#         cache[n] = (binary(n-1) + binary(n-2)) % 15746
#         return cache[n]

# print(binary(n)%15746)

binary_first  = 1
binary_second = 2
for _ in range(n-3):
    
    new = binary_first + binary_second
    binary_first  = binary_second
    binary_second = new %15746

if n == 1: print(1); exit()
elif n ==2: print(2); exit()
else:
    print((binary_first + binary_second)%15746)
