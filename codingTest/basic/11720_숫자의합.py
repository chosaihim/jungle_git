import sys  
input = sys.stdin.readline

N = int(input())
nums = input()

total = 0
for i in range(N):
    total += int(nums[i])

print(total)