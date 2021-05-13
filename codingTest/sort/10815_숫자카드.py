import sys
from collections import deque
input = sys.stdin.readline

n = int(input())
n_list = list(map(int,input().split()))
m = int(input())
m_list = list(map(int,input().split()))

n_list.sort()

def bin_search(n_list, m_card):
    pl = 0
    pr = len(n_list) - 1
    
    while True:
        pc = (pl+pr) // 2
        
        if n_list[pc] == m_card:
            return 1
        elif n_list[pc] < m_card:
            pl = pc + 1
        else:
            pr = pc - 1
            
        if pl > pr:
            break
        
    return 0
    
for m_card in m_list:
    print(bin_search(n_list,m_card), end = ' ')