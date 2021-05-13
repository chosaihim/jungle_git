#108ms
import sys
input = sys.stdin.readline

n = int(input())

def stars(n):
    result = [""] *n
    
    if n == 1: return "*"
    else:
        pattern = stars(n//3)
        len_pattern = len(pattern)
        
        for i in range(3):
            for j in range(3):
                for row in range(len_pattern):
                    if i == j == 1:
                        result[i*len_pattern + row] += " " * len_pattern
                    else: 
                        result[i*len_pattern + row] += pattern[row]
                
        return result
    
answer = stars(n)
for row in answer: print(row)


# #64ms
# a=int(input())
# def s(n):
#  if n==3:return['***','* *','***']
#  x=s(n//3)
#  y=list(zip(x,x,x))
#  for i in range(len(y)):y[i]=''.join(y[i])
#  z=list(zip(x,[' '*(n//3)]*(n//3),x))
#  for i in range(len(z)):z[i]=''.join(z[i])
#  return y+z+y
# print('\n'.join(s(a)))