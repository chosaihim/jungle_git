import sys
input = lambda: sys.stdin.readline().strip()

r,c = map(int,input().split())
a = [list(map(lambda x:ord(x)-65, input())) for i in range(r)]
ch=[0]*26

dx = [-1,0,1,0]
dy = [0,1,0,-1]

def dfs(x,y,z):
    global answer
    answer = max(answer,z)

    for i in range(4):
        nx = x+dx[i]
        ny = y+dy[i]

        if 0 <= nx < r and 0<= ny < c and ch[a[nx][ny]] == 0:
            ch[a[nx][ny]] = 1
            dfs(nx,ny,z+1)
            ch[a[nx][ny]]=0

answer =1 
ch[a[0][0]] =1
dfs(0,0,answer)

print(answer)


# 8 8
# ASWERHGC
# QWERHDLK
# ZKFOWOHK
# SALTPWOK
# BMDLKLKD
# ALSKEMFL
# GMHMBPTI
# DMNKJZKQ
#
# --> 20

# 10 10
# ASWERHGCFH
# QWERHDLKDG
# ZKFOWOHKRK
# SALTPWOKSS
# BMDLKLKDKF
# ALSKEMFLFQ
# GMHMBPTIYU
# DMNKJZKQLF
# HKFKGLKEOL
# OTOJKNKRMW
#
# --> 22