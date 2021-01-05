import sys
sys.stdin = open("input.txt", "r")
read = sys.stdin.readline

N, M = map(int, read().rstrip().split())

small_stones = list(int(read()) for _ in range(M))
print(small_stones)

def recur(n, i, count):
    print(n, i, count)
    if n == N:
        print(count)
        sys.exit()
    elif n > N:
        return
    else:
        count += 1
        if n+(i+1) not in small_stones:
            recur(n+(i+1), i+1, count)
        if i > 0 and n+i not in small_stones:
            recur(n+i, i, count)
        if i-1 > 0 and n+(i-1) not in small_stones:
            recur(n+(i-1), i-1, count)


recur(1, 0, 0)
print(-1)