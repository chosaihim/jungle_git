## 오답
# 에라토스테네스의 체로 소수로 이루어진 수의 배열을 만든다.
# 소수 배열에서 하나씩 꺼내 수를 하나씩 지운다.

def solution(arr):
    answer = 1
    
    arr.sort()
    
    if(arr[0] == 0):
        answer = 0
    
    for i in range(len(arr)):
        for j in range(i+1,len(arr)):
            if(arr[i] != 1 and arr[j] % arr[i] == 0):
                arr[j] //= arr[i]
    
    for num in arr:
        answer *= num
    
    return answer