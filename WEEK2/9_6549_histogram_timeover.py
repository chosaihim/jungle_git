import sys
sys.setrecursionlimit(10**8) # 10^8 까지 늘림.

def maxBox(_histogram):
    max_size = 0

    # print(f'histogram:{_histogram}')

    if(len(_histogram) == 1): return _histogram[0]
    
    min_height = min(_histogram)
    min_index  = _histogram.index(min_height)
    his_length = len(_histogram)
    max_size = max(max_size, min_height*his_length)
    # print(f'max_size:{max_size}')
    
    if not (min_index == 0): max_size= max(max_size,maxBox(_histogram[0:min_index]))
    if not (min_index == his_length -1): max_size= max(max_size,maxBox(_histogram[min_index+1:len(_histogram)]))
    # if not (min_index == len(_histogram)-1): max_size= max(max_size,maxBox(_histogram[min_index+1:len(_histogram)]))

    return max_size



while True:
    #input
    histogram = list(map(int, sys.stdin.readline().split()))

    #break condition
    if histogram[0] == 0 : break
    
    n = histogram[0]
    histogram = histogram[1:n+1]

    #print answer
    print(maxBox(histogram))
    histogram.clear()