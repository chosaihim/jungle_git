import sys  
n = list(map(int, sys.stdin.readline().split()))[0]

debug = False
original_n = n
cycle = 0

while True:
    a = 0; b = 0; new = 0

    if(n>9):
        a = n //10
        b = n % 10
    else:
        a = 0
        b = n
        
    sum_ab = a+ b

    new = b*10 + sum_ab %10

    if debug:
        print(f'a = {a}, b = {b}, a+b = {sum_ab}, new = {new}')
    
    n = new
    cycle += 1

    if(n == original_n): break

print(cycle)

