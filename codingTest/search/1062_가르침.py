import sys
input = sys.stdin.readline

n, k = list(map(int, input().split())) # n: number of cards, m: goal number
words = []
for i in range(n): words.append(input().rstrip('\n'))

print(n,k)
print(words)

# set으로 만들기
words_set = []
for word in words:
    print(list(word))
    print(set(list(word)))
    words_set.append(set(list(word)))
    print(words_set)
    
    