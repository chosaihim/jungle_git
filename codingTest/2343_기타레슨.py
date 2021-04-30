# 252ms
import sys
input = sys.stdin.readline

n, m = map(int, input().split())
lectures = list(map(int, input().split()))

def bin_search(m, lectures):
    pl = max(lectures)
    pr = 0
    for lecture in lectures: pr += lecture
    min_time = 9999999999
    
    while True:
        pc = (pl+pr) // 2
        
        sum = 0
        cd  = 1
        for lecture in lectures:
            sum += lecture
            if sum > pc:
                sum = lecture
                cd += 1

        if cd > m:
            pl = pc + 1
        else:
            min_time = min(min_time, pc)
            pr = pc -1
            
        if pl > pr:
            break
    
    return min_time

print(bin_search(m,lectures))



#130ms
# import bisect

# n, m = map(int, input().split())
# a = list(map(int, input().split()))

# out = [0 for _ in range(n)]
# out[0] = a[0]
# for i in range(1,n) :
# 	out[i] = out[i-1]+a[i]

# left = 0
# right = out[-1]
# while left < right :
# 	mid = (left+right)//2

# 	if mid == 0 :
# 		left = 1
# 		break

# 	count = 1
# 	cut = mid
# 	pos = 0
# 	while cut < out[-1] :
# 		count += 1
# 		tmp = bisect.bisect_right(out,cut)
# 		if tmp == pos :
# 			count = float('inf')
# 			break
# 		cut = out[tmp-1]+mid
# 		pos = tmp

# 	if count <= m :
# 		right = mid
# 	else :
# 		left = mid+1

# print(left)