# you can write to stdout for debugging purposes, e.g.
# print("this is a debug message")

def solution(A):

    ptr_front = 0
    ptr_back = len(A)-1 
    A.sort()

    while ptr_front < ptr_back :
        
        if A[ptr_front] == - A[ptr_back]:
            return A[ptr_back]
        elif abs(A[ptr_front]) > abs(A[ptr_back]):
            ptr_front += 1
        else:
            ptr_back -= 1

    return 0
