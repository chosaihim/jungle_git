num = int(input())
original = num
count = 0
for i in range(1000):
    if original == int(num) and i > 0:
        break
    if num < 10:
        num = str(num)
        num = num + num
        num = int(num) 
    else:
        num = str(num)
        newNum = int(num[0]) + int(num[-1])
        newNum = str(newNum)
        num = num[-1] + newNum[-1]
        num = int(num) 
        
    # print(num)
    count +=1 
    

print(count)