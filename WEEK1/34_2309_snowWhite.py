import sys

def find_dwarf(dwarf):
    dwarf.sort()
    h_sum = sum(dwarf)
    answer = []

    for i in range(8):
        for j in range(i+1,9):
            if((h_sum - dwarf[i] - dwarf[j]) == 100):
                answer.append(i)
                answer.append(j)
                return answer

dwarf =[]
for i in range(9):
    dwarf.append(int((sys.stdin.readline().split())[0]))

del_dwarf = find_dwarf(dwarf)
del dwarf[del_dwarf[1]]
del dwarf[del_dwarf[0]]  

for i in range(7):
    print(dwarf[i])