cache = [False] * 10001
start = [False] * 10001

def selfNumber(number):

    if not start[number]:
        start[number] = True
        total = 0
        
        str_number = str(number)
        for str_digit in str_number:
            total += int(str_digit)
        total += number
            
        if total <= 10000:
            cache[total] = True
            selfNumber(total)

for i in range(1,10000):
    selfNumber(i)

for i in range(1,10000):
    if not cache[i]:
        print(i)
    
