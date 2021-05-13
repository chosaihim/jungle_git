from collections import deque

def solution(n, k, cmd):
    answer = ''
    
    # queues
    front  = deque()
    back   = deque([i for i in range(n)])
    delete = deque()
    
    # first cursor
    cursor = k
    for _ in range(k):
        front.append(back.popleft())
    
    for c in cmd:
        print(c)
        if c[0] == "U":
            for i in range(int(c.split()[1])):
                if front: back.appendleft(front.pop())
                else: break
            
        elif c[0] == "D":
            for i in range(int(c.split()[1])):
                if back: front.append(back.popleft())
                else: break
            if not back: back.appendleft(front.pop())
            
        elif c[0] == "C":
            if back: delete.append(back.popleft())
            else: delete.append(front.pop())
            if not back: back.appendleft(front.pop())
            
        elif c[0] == "Z":
            alive = delete.pop()
            
            #goto front
            if back[0] > alive:
                if front:
                    for i in range(len(front)):
                        if front[i] > alive:
                            front.insert(i, alive)
                            break
                else:
                    front.append(alive)
            #goto back
            else:
                for i in range(1,len(back)+1):
                    if i == len(back):
                        back.append(alive)
                        break
                    elif back[i] > alive:
                        back.insert(i, alive)
                        break
            
            print("after Z")
            print(f'front:{front}')
            print(f'back:{back}')
            print(f'delete:{delete}')
                            
        # print()
        # print(f'front:{front}')
        # print(f'back:{back}')
        # print(f'delete:{delete}')

    ret = front + back
    print(ret)
        
    idx = 0
    for i in range(n):
        if i in ret:
            answer += 'O'
        else:
            answer += 'X'
    return answer


n = 13
k = 2
cmd = ["D 2","C","U 3","C","D 4","C","U 2","Z","Z","Z","C", "C", "C"]

n = 5
cmd = ["U 3", "C", "C", "C", "D 3", "C", "D 3", "U 3"]

print(solution(n, k, cmd))