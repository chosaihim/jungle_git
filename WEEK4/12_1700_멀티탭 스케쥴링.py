import sys
input = sys.stdin.readline

#input
N, K = map(int,input().split()) # N: hole_num K:usage
plugItem = list(map(int,input().split()))


left_items = [0] * (K+1)
for item in plugItem:
    left_items[item] += 1

onPlugNow = []

plug = 0
unplug = 0
for now in range(len(plugItem)):
    item = plugItem[now]
    if plug < N and item not in onPlugNow:
        onPlugNow.append(item)
        plug += 1
        left_items[item] -= 1
    elif item in onPlugNow:
        left_items[item] -= 1
        continue
    else:
        unplug += 1
        for i in onPlugNow:
            if not left_items[i]:
                onPlugNow.remove(i)
                plug -= 1
                break
        if plug == N:
            unPlugCandidates = onPlugNow.copy()
            for check in plugItem[now+1:]:
                if len(unPlugCandidates) == 1:
                    onPlugNow.remove(unPlugCandidates[0])
                    plug -= 1
                    break
                if check in unPlugCandidates:
                    unPlugCandidates.remove(check)
                

        onPlugNow.append(item)
        plug += 1

print(unplug)