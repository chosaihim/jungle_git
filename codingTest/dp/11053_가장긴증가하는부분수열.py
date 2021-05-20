#196ms
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int,input().split()))
dp = [1] * n


for i in range(n):
    for j in range(i+1):
        if a[j] < a[i]:
            dp[i] = max(dp[i], dp[j]+1)

print(max(dp))

#풀이
N = int(input())
li = list(map(int,input().split()))
dp = [li[0]]

for i in range(1,N):
    if li[i] > dp[-1]:
        dp.append(li[i])
    else:
        j = len(dp)-1
        while j > 0:
            if dp[j-1] < li[i]:
                break
            j -= 1
        dp[j] = li[i]
print(len(dp))