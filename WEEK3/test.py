import sys
read = sys.stdin.readline
sys.setrecursionlimit(10**5)

N = int(read())
isParent = [False] * (N+1)
tree = [[] for _ in range(N+1)]
# 부모들의 자식 합
max_sum = [[] for _ in range(N+1)]


for _ in range(N-1):
    parent, child, value = map(int,read().rstrip().split())
    tree[parent].append((child,value))
    isParent[parent] = True

def dfs(node,value):
    global p
    #끝에 도달했으면, 합산 추가!
    if len(tree[node]) == 0:
        ans.append((value))
    
    for child,child_value in tree[node]:
        # 자식들에게 
        dfs(child,value+child_value)
        # 부모한테 돌아왔으면, 자식들의 합을 넣어준다.
        if node == p:
            max_sum[p].append(max(ans))
            ans.clear()

for i in range(N+1):
    if isParent[i]:
        p = i
        ans = []
        dfs(i,0)

# max_sum을 정렬을 해보자 그렇게해서 앞에 두놈만 더한다!
result = -1
for i in range(len(max_sum)):
    # 값이 2개 이상 있는 녀석들 중 가장 큰 두개의 값만 빼낸다.
    if isParent[i] and len(max_sum[i]) >= 2:
        max_sum[i] = sorted(max_sum[i], reverse=True)
        summ = max_sum[i][0] + max_sum[i][1]
        result = max(summ,result)
# print(max_sum)
print(result)