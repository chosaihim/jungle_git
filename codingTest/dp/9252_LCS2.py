#848ms
import sys
input = sys.stdin.readline

str1 = input().strip()
str2 = input().strip()

dp = [[0] * (len(str1)+1) for _ in range(len(str2)+1)]
lcs = [[""] * (len(str1)+1) for _ in range(len(str2)+1)]

for i in range(1,len(str2)+1):
    for j in range(1,len(str1)+1):
        if str2[i-1] == str1[j-1]:
            # dp[i][j] = max(dp[i][j-1], dp[i-1][j])
            # if dp[i-1][j-1]+1 >= dp[i][j]:
            dp[i][j] = dp[i-1][j-1]+1
            lcs[i][j] = lcs[i-1][j-1] + str2[i-1]
        else:
            if dp[i][j-1] > dp[i-1][j]:
                dp[i][j] = dp[i][j-1]
                lcs[i][j] = lcs[i][j-1]
            else:
                dp[i][j] = dp[i-1][j]
                lcs[i][j] = lcs[i-1][j]
    
print(dp[-1][-1])
print(lcs[-1][-1])


#92ms
import sys


def solve():
    s1 = input()
    s2 = input()

    s1, s2 = (s1, s2) if len(s1) < len(s2) else (s2, s1)

    # idx[c]는 문자c가 s2에서 나타나는 위치의 리스트
    idx = {chr(ord('A') + i): [] for i in range(26)}
    for i, c in enumerate(s2):
        idx[c].append(i)
    mem = []
    traceback = []
    for i, c in enumerate(s1):
        if idx[c]:
            mem.append(idx[c][0])
            traceback.append((i, 0))
            break
    for j in range(i + 1, len(s1)):
        c = s1[j]
        idx_iter = iter(idx[c])
        new_mem = mem[:]
        try:
            cur_idx = next(idx_iter)
            if cur_idx < mem[0]:
                new_mem[0] = cur_idx
                traceback.append((j, 0))
            for k in range(len(mem) - 1):
                while cur_idx <= mem[k]:
                    cur_idx = next(idx_iter)
                if cur_idx < mem[k + 1]:
                    new_mem[k + 1] = cur_idx
                    traceback.append((j, k + 1))
            while cur_idx <= mem[-1]:
                cur_idx = next(idx_iter)
            new_mem.append(cur_idx)
            traceback.append((j, len(mem)))
        except StopIteration:
            pass
        mem = new_mem
    cur_len = len(mem)
    print(cur_len)
    ans = []
    selected = [False] * len(s1)
    for j, i in traceback[::-1]:
        if i == cur_len - 1 and not selected[j]:
            cur_len -= 1
            selected[j] = True
            ans.append(s1[j])
            if cur_len == 0:
                break
    if ans:
        print(''.join(ans[::-1]))


solve()


#172
def s():
    s1, s2 = input(), input()
    dp = [0] * 1000
    dp2 = [""] * 1000
    for i in range(len(s1)):
        max_dp = 0
        ch = ""
        for j in range(len(s2)):
            if max_dp < dp[j]:
                max_dp = dp[j]
                ch = dp2[j]
            elif s1[i] == s2[j]:
                dp[j] = max_dp + 1
                dp2[j] = ch + s2[j]
    tmp, idx = 0, 0
    for i in range(1000):
        if tmp < dp[i]:
            tmp = dp[i]
            idx = i
    print(dp[idx])
    print(dp2[idx])
s()