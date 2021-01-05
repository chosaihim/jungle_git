import sys

# cities = int((sys.stdin.readline().split())[0])

queue   = []
left    = []
impos   = []
in_data = [0,1,2,3]
costs   = [[0,1,1,1],[1,0,1,1],[1,1,0,1],[1,1,1,0]]
check   = [[0,1,1,1],[1,0,1,1],[1,1,0,1],[1,1,1,0]]

left = in_data
check = costs
queue.append(left.pop(0))

print("left: ", left)

def search(cost_len):

    while len(left) > 0:

        if(costs[queue[-1]][left[0]]):
            queue.append(left.pop(0))
        
        print("left len: ", len(left))
        print("queue: ", queue)
        print("left: ", left)



    return 0

search(4)


        



