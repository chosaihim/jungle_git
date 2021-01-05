arr = [1,2,3,4,5,6]
answer = []
cache = []


def dep2(array, depth, limit):
    
    j = 0
    if(depth == limit):
        # print(answer)
        None
    else:
        for i in (array):
            if(i in cache):
                None
            else:
                answer.append(i)
                cache.append(i)
                dep2(array,depth+1,limit)
                answer.remove(i)
                cache.remove(i)

                if depth == 0:
                    cache.append(i)

dep2(arr,0,6)
