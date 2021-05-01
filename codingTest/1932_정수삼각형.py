import sys
input = sys.stdin.readline

n = int(input())
triangle = [list(map(int,input().split())) for _ in range(n)]


def max_sum(triangle):
    
    for i in range(1,len(triangle)):
        for j in range(i+1):
            if j == 0: triangle[i][j] += triangle[i-1][j]
            elif j == i: triangle[i][j] += triangle[i-1][j-1]
            else: triangle[i][j] += max(triangle[i-1][j-1], triangle[i-1][j])
        
        # print(triangle)
        
    return max(triangle[len(triangle)-1])
        
print(max_sum(triangle))

# # Faster
# def solution():
#     import sys
#     n = int(input())
#     triangle =[]
#     for _ in range(n):
#         triangle.append(list(map(int, sys.stdin.readline().rstrip().split())))
                   
#     accum = []
#     for i in range(n):
#         accum = [max(a+c, b+c) for a,b,c in zip([0]+accum, accum+[0], triangle[i])]
#     print(max(accum))

# solution()