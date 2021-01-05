import sys
debugFlag = False

n = int(input())    # 1 <= N <= 500,000

front    = 0
rear     = 0
capacity = n
no       = n
que      = [i+1 for i in range(n)]

while True:

    # 예외처리
    if(n==1): que[front] = 1; break

    # print(f'no:{no}')
    # delete the first num(deque)
    que[front] = 0
    
    front += 1
    no    -= 1

    if front == capacity:
        front = 0


    if no == 1:
        break

    # move first to rear
    # if( que[rear] and que[front]):
    que[rear] = que[front]
    que[front] = 0


    front += 1
    rear  += 1

    if front == capacity:
        front = 0
    if rear == capacity:
        rear = 0

    # print(que)


print(que[front])

