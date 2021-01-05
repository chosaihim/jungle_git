import sys
from collections import deque
# debugFlag = True
debugFlag = False


n = list(map(int, sys.stdin.readline().split()))[0]
que = deque([[0,0],])

# apples = deque()
k = list(map(int, sys.stdin.readline().split()))[0] # number of apples
apples = []
for _ in range(k):
    apples.append(list(map(int, sys.stdin.readline().split()))[:])
for i in range(k):
    apples[i][0] -= 1; apples[i][1] -= 1
    
if debugFlag: print(apples)





head = [0,0]
dire = [0,1]
rdlu = 0 # direction % 4 = 0 right 1 down 2 left 3 up
time = 0
t_move = 0
crashFlag = False
RorL = 0

l = list(map(int, sys.stdin.readline().split()))[0] # number of turns

moves = []
for _ in range(l):
    moves.append(list(map(str, sys.stdin.readline().split())))

t_move = 0
index = 0
while True:



    time   += 1

    # print(f'time:{time} index:{index}, t_move:{t_move}')

    if index < l and time == t_move+1:
        sec  = moves[index][0]
        turn = moves[index][1]

        t_move = int(sec)
        RorL   = 1 if turn == 'D' else -1
        # print(f'RorL: {RorL}')


    
        
    # print(f'time:{time}, t_move:{t_move}')


    head[0] += dire[0]
    head[1] += dire[1]

    if (head in que) or head[0] < 0 or head[0] >=n or head[1] < 0 or head[1] >=n:
        # print(f'crashed, time {time}')
        crashFlag = True
        break

    que.append(head[:])

    if(head in apples):
        # print("met Apple")
        apples.remove(head)
    else:
        que.popleft()

    # print(que)


    if index < l and time == t_move:
        # print("make Turn!")

        #방향전환
        rdlu = (rdlu + RorL) %4
        if(rdlu == 0):     dire = [ 0, 1]
        elif(rdlu == 1): dire = [ 1, 0]
        elif(rdlu == 2): dire = [ 0,-1]
        else:            dire = [-1, 0]

        # print(dire)
        
        index += 1

print(time)

