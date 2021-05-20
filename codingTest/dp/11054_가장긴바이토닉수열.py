# #120ms
# import sys
# input = sys.stdin.readline

# n = int(input())
# a = list(map(int,input().split()))

# front_dp = [1] * n
# front_a  = [a[0]]
# back_dp  = [1] * n
# back_a   = [a[-1]]

# for i in range(1,n):
#     #from front
#     if a[i] > front_a[-1]:
#         front_a.append(a[i])
#     else:
#         j = len(front_a) - 1
#         while j > 0:
#             if front_a[j-1] < a[i]:
#                 break
#             j -= 1
#         front_a[j] = a[i]

#     front_dp[i] = len(front_a)
    
#     #from back
#     if a[-1-i] > back_a[-1]:
#         back_a.append(a[-1-i])
#     else:
#         j = len(back_a) - 1
#         while j > 0:
#             if back_a[j-1] < a[-1-i]:
#                 break
#             j -= 1
#         back_a[j] = a[-1-i]

#     back_dp[i] = len(back_a)

# # back_dp.reverse()
# max_sum = 0
# for i in range(n):
#     max_sum = max(max_sum, front_dp[i] + back_dp[-i-1])
# print(max_sum-1)


#함수로 다시 짜보기
import sys
input = sys.stdin.readline

def find_sequence_length(a_seq, n):
    len_dp = [1] * n
    dp = [a_seq[0]]
    
    for i in range(1,n):
        if a_seq[i] > dp[-1]:
            dp.append(a_seq[i])
        else:
            j = len(dp) - 1
            while j>0 and dp[j-1] >= a_seq[i]:
                j -= 1
            dp[j] = a_seq[i]
            
        len_dp[i] = len(dp)
    return len_dp


# input
n = int(input())
a = list(map(int,input().split()))

front_len = find_sequence_length(a,n)
a.reverse()
back_len  = find_sequence_length(a,n)

# print
max_sum = 0
for i in range(n):
    max_sum = max(max_sum, front_len[i] + back_len[-i-1])
print(max_sum-1)
