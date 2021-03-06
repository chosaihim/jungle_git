#140ms
import sys
import re
input = sys.stdin.readline

n = int(input())
count = 0

for _ in range(n):
    no_repeated = list(re.sub(r'(?s)(.)(?=\1)','', input().strip()))
    if len(no_repeated) == len(set(no_repeated)): count += 1
        
print(count)

#56ms
result = 0
for i in range(int(input())):
    word = input()
    if list(word) == sorted(word, key=word.find):
        result += 1
print(result)