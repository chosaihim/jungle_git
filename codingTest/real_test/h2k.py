#1
def solution(arr):
    answer = False
    
    if(len(arr) == len(set(arr))):
        if(max(arr) == len(arr)):
            answer = True

    return answer


#2
## solution 
def solution(board):
    for row in range(1,len(board)):
        for col in range(1,len(board[0])):
            if board[row][col] == 1:
                if (board[row-1][col] > 0 ) and (board[row][col-1] > 0):
                    board[row][col] = min(board[row-1][col-1],board[row-1][col],board[row][col-1]) + 1
    
    max_len = max(map(max, board))
    return max_len ** 2

## END OF solution


## submitted
def solution(board):
    answer = 0
    
    max_len = min(len(board),len(board[0]))
    # print(max_len)
    
    left = 0; right = max_len
    
    while True:
        mid = (left + right)//2
        # print(f'mid: {mid}')
        
        if(GetSquare(board, mid)):
            left = mid + 1
            answer = mid
        else:
            right = mid - 1
        
        if left > right:
            break
    
    return answer*answer


def GetSquare(board, n):
    if n == 0:
        return True
    
    for i in range(len(board)-n+1):
        for j in range(len(board[0])-n+1):
            # print(f'i: {i}, j:{j}')
            
            test = []
            flag = False
            
            for row in range(i,i+n):
                for col in range(j, j+n):
                    if board[row][col] == 0:
                        flag = True
                        break
                    else:
                        if(row == i+n-1) and (col == j+n-1):
                            return True
                if(flag):
                    break
    return False
## END OF submitted


#3
def solution(A, B):
    answer = 0
    
    A.sort()
    B.sort()
    
    a_index = 0
    
    for b in B:
        if b > A[a_index]:
            answer += 1
            a_index += 1
    
    return answer

#4
# -- 코드를 입력하세요
# SELECT BRANCH_ID, SUM(SALARY)
# FROM EMPLOYEES
# GROUP BY BRANCH_ID
# ORDER BY BRANCH_ID