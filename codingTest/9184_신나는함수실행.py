import sys
input = sys.stdin.readline

cache = [[[0]*101 for _ in range(101)] for _ in range(101)]

def w(a,b,c):
    
    if cache[a+50][b+50][c+50]: return cache[a+50][b+50][c+50]
    
    if a <= 0 or b <= 0 or c <= 0:
        cache[a+50][b+50][c+50] = 1
    elif a > 20 or b > 20 or c > 20:
        cache[a+50][b+50][c+50] =  w(20,20,20)
    elif a < b and b < c:
        cache[a+50][b+50][c+50] = w(a, b, c-1) + w(a, b-1, c-1) - w(a, b-1, c)
    else:
        cache[a+50][b+50][c+50] = w(a-1, b, c) + w(a-1, b-1, c) + w(a-1, b, c-1) - w(a-1, b-1, c-1)

    return cache[a+50][b+50][c+50]

while True:
    a, b, c = map(str,input().split())
    
    if a == '-1' and b == '-1' and c == '-1':
        break
    
    # print(w(int(a),int(b),int(c)))
    
    answer = 'w(' + a + ', ' + b + ', ' + c + ') = ' + str(w(int(a),int(b),int(c)))
    print(answer)