#1
# import sys, math
# n = int((sys.stdin.readline().split())[0])

# def hanoi(layer,start,des):
    
#     move = 0; empty = 0

#     # if(start==1 and des == 2): empty = 3
#     # elif(start == 2 and des == 3): empty = 1
#     # else: empty = 2

#     empty = 6 - start - des

#     if layer == 1:
#         print(start, des)
#     else:
#         move += hanoi(layer-1,start,empty)
#         print(start, des)
#         move += hanoi(layer-1,empty,des)
    
#     move += 1
  
#     return move


# if(n < 21):
#     print(int(math.pow(2,n))-1)
#     hanoi(n,1,3)
# else:
#     print(int(math.pow(2,n))-1)

##2
import sys, math
n = int((sys.stdin.readline().split())[0])

def hanoi(layer,start,des):
    
    move = 0; empty = 0
    empty = 6 - start - des

    if layer == 1:
        print(start, des)
    else:
        hanoi(layer-1,start,empty)
        print(start, des)
        hanoi(layer-1,empty,des)  
    return None


if(n < 21):
    print(int(math.pow(2,n))-1)
    hanoi(n,1,3)
else:
    print(int(math.pow(2,n))-1)

