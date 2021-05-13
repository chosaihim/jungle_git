import sys
input = sys.stdin.readline

n = int(input())

def sum_digits(number):
    num = str(number)
    total = 0
    for i in range(len(num)):
        total += int(num[i])
    return total 
    

for number in range(1,n+1):
    if(n == number + sum_digits(number)):
        print(number)
        break
    if(number == n):
        print(0)
        
        
# solution!!
# import sys

# def solve():
#     n = sys.stdin.readline().strip()
#     max_diff = len(n)*9
#     n = int(n)

#     if n == 1:
#         return(0)

#     ans = 0
#     for i in range(max(n - max_diff, 1), n + 1):
#         if i + sum(map(int, str(i))) == n:
#             ans = i
#             break
#     return ans

# print(solve())

