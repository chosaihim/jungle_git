import sys
input = sys.stdin.readline

n, m = map(int, input().split())
numbers = [list(map(int,input().split())) for _ in range(n)]

print(numbers)

def bfs(row, col):
    dir = [[0,1],[1,0]]
    queue = [[row,col,numbers[row][col]]]
    max_total = 0
    
    # ◻︎◻︎◻︎◻︎   ◻︎◻︎   ◻︎
    #       ◻︎◻︎    ◻︎◻︎◻︎ 
    for i in range(3):
        new_q = []
        
        for r, c, total in queue:
            
            for dr, dc in dir:
                nr = r + dr; nc = c + dc
                
                if nr < n and nc < m:
                    print(f'nr:{nr}, nc:{nc}, total:{total+numbers[nr][nc]}')
                    if i == 2:
                        max_total = max(max_total,total+numbers[nr][nc])
                    else:
                        new_q.append([nr,nc,total+numbers[nr][nc]])

        queue = new_q
        
    # ◻︎◻︎
    # ◻︎◻︎ 
    if row + 1 < n and col + 1 < n:
        max_total = max(max_total, numbers[row][col]+numbers[row+1][col]+numbers[row][col+1]+numbers[row+1][col+1])
    
    #  ◻︎
    # ◻︎◻︎◻︎
    if row + 2 < n:
        total = numbers[row][col] + numbers[row+1][col] + numbers[row+2][col]
        if col - 1 > 0:
            max_total = max(max_total,total+numbers[row+1][col-1])
        if col + 1 < m:
            max_total = max(max_total,total+numbers[row+1][col+1])
    
    if col + 2 < m:
        total = numbers[row][col] + numbers[row][col+1] + numbers[row][col+2]
        if row - 1 > 0:
            max_total = max(max_total,total+numbers[row-1][col+1])
        if row + 1 < n:
            max_total = max(max_total,total+numbers[row+1][col+1])
    
    
    return max_total    

answer = 0
for row in range(n):
    for col in range(m):
        print(f'n:{row}, m:{col}')
        answer = max(answer, bfs(row,col))

# answer = bfs(0,0)
print(answer)
#5 5
1 2 3 4 5
5 4 3 2 1
2 3 4 5 6
6 5 4 3 2
1 2 1 2 1