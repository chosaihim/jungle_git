import sys

def find_fake(dwarfs_list):
    dwarfs_list.sort()
    h_sum = sum(dwarfs_list)
    for i in range(8):
        for j in range(i+1,9):
            if (h_sum - dwarfs_list[i] - dwarfs_list[j]) == 100 :
                del dwarfs_list[j]
                del dwarfs_list[i]
                return dwarfs_list

##MAIN##
#get input
dwarf =[]
for i in range(9):
    dwarf.append(int((sys.stdin.readline().split())[0]))
#get and print answer
answer = find_fake(dwarf)
for i in range(7):
    print(answer[i])



