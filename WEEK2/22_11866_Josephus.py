import sys
debugFlag = True
# debugFlag = False

n, k= list(map(int, sys.stdin.readline().split()))

front    = 0
rear     = 0
capacity = n
no       = n
que      = [i+1 for i in range(n)]

answer   = []
cnt      = 0

while True:

    cnt += 1

    if no == 0: break

    if cnt == k: 
        cnt = 0
        answer.append(que[front])
        que[front] = 0
        
        front += 1
        no    -= 1

        if front == capacity: front = 0

    else:         
        que[rear] = que[front]

        if debugFlag: 
            if(front != rear): que[front] =0

        front += 1; rear  += 1

        if front == capacity: front = 0
        if rear == capacity:  rear = 0

    # print(que)
# print(answer)

print("<",end=''); print(", ".join(map(str, answer)),end=''); print(">");
    