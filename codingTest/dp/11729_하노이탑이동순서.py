import sys
input = sys.stdin.readline

layer = int(input())
move = []

def hanoi(start, end, layer):
    
    stopBy = 6 - start - end
    
    if layer == 1:
        # move.append((start,end))
        print(start,end)
    else:
        hanoi(start, stopBy, layer-1)
        print(start,end)
        # move.append((start,end))
        hanoi(stopBy, end, layer-1)
        

print(2**layer-1)
hanoi(1,3,layer)
# print(len(move))
# for start, end in move:
    # print(start, end)