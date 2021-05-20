#76ms
import sys
input = sys.stdin.readline

num_weights = int(input())
weights     = list(map(int,input().split()))
num_beads   = int(input())
beads       = list(map(int,input().split()))

weight_combination = {0}

for weight in weights:
    temp_weight = []
    for combination in weight_combination:
        temp_weight.append(combination + weight)
        temp_weight.append(abs(combination-weight))
    for temp in temp_weight:
        weight_combination.add(temp)


for bead in beads:
    print("Y", end=' ') if bead in weight_combination else print("N", end=' ')
    

#64ms
input()
s = []
for k in map(int, input().split(' ')):
    for i in range(len(s)):
        s.append(k+s[i])
        s.append(abs(k-s[i]))
    s.append(k)
    s=list(set(s))
input()
for k in map(int, input().split(' ')):
    print("Y" if k in s else "N",end=' ')
    

#68ms dp
N = int(input())
weights = list(map(int, input().split()))
M = int(input())
beads = list(map(int, input().split()))
sumN = sum(weights)
dp = [[False for _ in range(sumN+1)] for k in range(N+1)]

def solve(row, col):
    if dp[row][col]:
        return
    else:
        dp[row][col] = True
    if row == N:
        return
    solve(row+1, abs(col-weights[row]))
    solve(row+1, col)
    solve(row+1, col+weights[row])
solve(0, 0)

res = []
for i in range(M):
    if sumN < beads[i]:
        res.append("N")
        continue
    if dp[N][beads[i]]:
        res.append("Y")
    else:
        res.append("N")

for i in res:
    print(i, end=" ")