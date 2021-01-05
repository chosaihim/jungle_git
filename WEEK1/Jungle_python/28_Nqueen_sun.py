debug = False
n = int(input())
chess = [None for i in range(n)]

def nqueen(depth:int, chess:list):
    global cnt
    if n == depth: 
        cnt += 1
        
    for v in range(n): # 
        for idx in range(depth):
            if v == chess[idx] or abs(idx - depth) == abs(v - chess[idx]):
                break
        else:
            chess[depth] = v 
            nqueen(depth+1, chess)

cnt = 0
chess[0] = 0
nqueen(0,chess)
print(cnt)