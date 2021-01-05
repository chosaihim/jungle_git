import sys
n      = list(map(int, sys.stdin.readline().split()))[0]
a_list = list(map(int, sys.stdin.readline().split()))
m      = list(map(int, sys.stdin.readline().split()))[0]
b_list = list(map(int, sys.stdin.readline().split()))

a_list.sort()

def bin_search(a, key):
    pl = 0          # 검색 범위의 맨 앞 원소 인덱스
    pr = len(a) - 1 # 검색 범위의 맨 끝 원소의 인덱스

    while True:
        pc = (pl+pr)//2     #중앙 원소의 인덱스

        if a[pc] == key:    
            # return pc       #검색 성공
            return 1
        elif a[pc] < key:   
            pl = pc + 1     # 검색 범위를 뒤쪽 절반으로
        else:               
            pr = pc -1      # 검색 범위를 앞쪽 절반으로
        
        if pl > pr:
            break

        # return -1   # 검색실패
    return 0


for b in b_list:
    print(bin_search(a_list,b))