from copy import deepcopy

# def solution(board):
#     dp = deepcopy(board)
    
#     for row in range(1,len(board)):
#         for col in range(1,len(board[0])):
#             if board[row][col] == 1:
#                 if (board[row-1][col] == 1) and (board[row][col-1] ==1):
#                     dp[row][col] = min(dp[row-1][col-1],dp[row-1][col],dp[row][col-1]) + 1
    
#     max_len = max(map(max, dp))
#     return max_len ** 2


def solution(board):
    for row in range(1,len(board)):
        for col in range(1,len(board[0])):
            if board[row][col] == 1:
                if (board[row-1][col] > 0 ) and (board[row][col-1] > 0):
                    board[row][col] = min(board[row-1][col-1],board[row-1][col],board[row][col-1]) + 1
    
    max_len = max(map(max, board))
    return max_len ** 2


board = [[0,1,1,1],[1,1,1,1],[1,1,1,1],[0,0,1,0]]
print(solution(board))