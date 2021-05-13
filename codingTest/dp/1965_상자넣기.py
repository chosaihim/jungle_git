#216ms
import sys
input = sys.stdin.readline

n = int(input())
boxes = list(map(int,input().split()))

def boxPutting(boxes):
    dp = [1] * len(boxes)
    
    for i in range(len(boxes)):
        for j in range(i):
            if boxes[j] < boxes[i]:
                dp[i] = max(dp[i], dp[j]+1)
        
    
    return max(dp)

print(boxPutting(boxes))


#60ms
# import bisect as b
# input()
# s,l=[*map(int,input().split())],[]
# for i in s:
#     j=b.bisect_left(l,i)
#     if j==len(l):l+=[i]
#     else:l[j]=i
# print(len(l))