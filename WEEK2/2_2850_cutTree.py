import sys,math
debugFlag = False

def cutting(trees, desired):
    lowest  = 0          # 검색 범위의 맨 앞 원소 인덱스
    highest = max(trees) # 검색 범위의 맨 끝 원소의 인덱스
    cutted  = []
    ok_cut  = 0

    while True:
        sum_cutted = 0
        cutted.clear()

        middle = (lowest+highest)//2        #현재 날의 위치
        if debugFlag: print(f'middle:{middle}, lowest:{lowest}, highest:{highest}')

        #현재 날로 자른 나무 조각들의 합
        for tree in trees:
            if not (tree - middle)<0: cutted.append(tree-middle)
        sum_cutted = sum(cutted)
        if debugFlag: print(f'sum: {sum_cutted}, desired = {desired}')    

        # 잘린 나무 조각의 합이 
        if sum_cutted == desired:   #딱 원하는 만큼이면 
            ok_cut = middle
            break
        elif sum_cutted < desired: # 딱 원하는 것보다 적으면
            highest = middle -1    # 검색 범위를 아래쪽 절반으로
        else:                      # 원하는 것보다 많으면
            lowest  = middle +1    # 검색 범위를 위쪽 절반으로
            ok_cut = max(ok_cut,middle)
        if  lowest > highest:      # 검색실패
            break                   

        if debugFlag: print(f'ok_cut: {ok_cut}')

    return ok_cut




tree_num, des_len = list(map(int, sys.stdin.readline().split()))
trees = list(map(int, sys.stdin.readline().split()))

if(debugFlag): print(f'tree_num:{tree_num}, des_len:{des_len}, trees:{trees}')

print(cutting(trees, des_len))
