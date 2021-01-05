import sys
sys.setrecursionlimit(10**6)
    
def maxBox(start,end):
    max_size = 0

    his_length = end - start
    if(his_length == 1): return histogram[start]

    temp_histo = histogram[start:end]

    min_height = min(temp_histo)
    min_index  = temp_histo.index(min_height) + start
    max_size   = max(max_size, min_height * his_length)
    # print(f'min_height:{min_height}, max_size:{max_size}')
    # print(f'min_index:{min_index}, {start}:{min_index} vs {min_index+1}:{end}')

    del temp_histo
    
    if not (min_index == start): max_size= max(max_size,maxBox(start,min_index))
    if not (min_index == end-1): max_size= max(max_size,maxBox(min_index+1, end))

    return max_size




while True:
    #input
    histogram = list(map(int, sys.stdin.readline().split()))

    #break condition
    if histogram[0] == 0 : break    
    n = histogram[0]

    #print answer
    print(maxBox(1,len(histogram)))
    del histogram