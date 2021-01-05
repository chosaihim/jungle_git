import sys  
arr1 = list(map(str, sys.stdin.readline().split()))[0]
arr2 = list(map(str, sys.stdin.readline().split()))[0]

longer = arr1
shorter = arr2

if(len(arr1) < len(arr2)):
    longer  = arr2
    shorter = arr1

Flag_find = False
shorter_len = len(shorter)
for str_len in range(shorter_len):
    for str_start in range(shorter_len - str_len):
        comp_str = shorter[str_start:str_start+shorter_len]

        if(comp_str in longer):
            print(len(comp_str))
            print(comp_str)
            Flag_find = True
            break
    
    if(Flag_find): break
