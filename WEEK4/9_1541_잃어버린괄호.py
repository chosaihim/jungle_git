import sys
input = sys.stdin.readline

#input
equation = list(input())


subMode = 0  # 0 add 1 sub
currentNum_str = ''
total = 0
for eq in equation:

    if( eq == '-'):
        if subMode: total -= int(currentNum_str)
        else: total += int(currentNum_str)

        subMode = 1
        currentNum_str = ''

    elif( eq == '+'):
        if subMode: total -= int(currentNum_str)
        else: total += int(currentNum_str)        

        currentNum_str = ''

    else:
        currentNum_str += eq


if subMode: print(total-int(currentNum_str))
else: print(total+int(currentNum_str))