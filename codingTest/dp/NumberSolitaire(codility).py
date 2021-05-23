def solution(A):
    
    dp = [A[0]]*len(A)

    for i in range(1,len(A)):
        dp[i] = dp[i-1]+A[i]
        for sub in range(2,7):
            if i-sub < 0:
                break
            dp[i] = max(dp[i],dp[i-sub]+A[i])
    
    return dp[-1]



######
A = [1, -2, 0, 9, -1, -2]
A = [-2,-1,1,-2,-2,-1,-1,-2,-2]
print(solution(A))



# faster solution
def solution(A):
    N = len(A)
    answer = [A[0]] * (N + 6)

    for i in range(1, N):
        answer[i + 6] = max(answer[i : i + 6]) + A[i]

    return answer[-1]

# mine copying
def solution(A):
    
    dp = [A[0]]*(len(A) + 5)

    for i in range(1, len(A)):
        dp[i + 5] = max(dp[i-1: i+5]) + A[i]
    
    return dp[-1]