import sys
input = sys.stdin.readline

n = int(input())

five  = n//5
total = 0

while five >= 0:
    left = n - 5 * five
    if left % 3 == 0:
        three = left//3 
        total = five + three
        break

    five -= 1

print(-1 if total>=10**10 else total)

