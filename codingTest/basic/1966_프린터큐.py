#76ms
import sys
input = sys.stdin.readline


testcase = int(input())

for _ in range(testcase):
    m, n = map(int, input().split())
    queue = list(map(int, input().split()))
    num_queue = [i for i in range(m)]
    count = 0
    
    while queue:
        max_priority = max(queue)
        priority = queue.pop(0)
        order    = num_queue.pop(0)
        
        if priority != max_priority:
            queue.append(priority)
            num_queue.append(order)
        else:
            count += 1
            if order == n:
                print(count)
                break