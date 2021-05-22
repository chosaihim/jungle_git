import sys
input = sys.stdin.readline

n, m, x, y, k = map(int, input().split())
board = [list(map(int,input().split())) for _ in range(n)]
directions = list(map(int,input().split())) #동쪽은 1, 서쪽은 2, 북쪽은 3, 남쪽은 4

dice = {'bottom':0, 'up':0, 'top':0, 'down':0, 'left':0, 'right': 0}


def roll_dice(direction):
    if direction == 1: #East
        temp = dice['bottom']
        dice['bottom'] = dice['right']
        dice['right'] = dice['top']
        dice['top'] = dice['left']
        dice['left'] = temp
    elif direction == 2: #West
        temp = dice['bottom']
        dice['bottom'] = dice['left']
        dice['left'] = dice['top']
        dice['top'] = dice['right']
        dice['right'] = temp
    elif direction == 3: #North
        temp = dice['bottom'] 
        dice['bottom'] = dice['up']
        dice['up'] = dice['top']
        dice['top'] = dice['down']
        dice['down'] = temp
    else:   #South
        temp = dice['down']
        dice['down'] = dice['top']
        dice['top'] = dice['up']
        dice['up'] = dice['bottom']
        dice['bottom'] = temp



for direction in directions:
    new_x = x; new_y = y 
    if direction == 1:   #East
        new_y = y + 1
    elif direction == 2: #West
        new_y = y - 1
    elif direction == 3: #North
        new_x = x - 1
    else:                #South
        new_x = x + 1

    if 0 <= new_x < n and 0 <= new_y < m:
        x = new_x; y = new_y
        roll_dice(direction)
        
        if board[new_x][new_y] == 0:
            board[new_x][new_y] = dice['bottom']
        else:
            dice['bottom'] = board[new_x][new_y]
            board[new_x][new_y] = 0
    
        print(dice['top'])
    