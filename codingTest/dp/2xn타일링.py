def solution(n):
    answer = 0
    
    dp = [1] * (n+1)
    
    if n > 1:
        for i in range(2,n+1):
            dp[i] = dp[i-2]% 1000000007 + dp[i-1]% 1000000007
    
    answer = dp[n] % 1000000007
    return answer


# 참고코드
def solution(n):
    a, b = 1, 1
    for i in range(1, n):
        a, b = b, (a + b) % 1000000007
    return b