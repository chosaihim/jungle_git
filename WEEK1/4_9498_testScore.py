import sys  
a = list(map(int, sys.stdin.readline().split()))
score = a[0]

if (score>=90):
    print("A")
elif(score>=80):
    print("B")
elif(score>=70):
    print("C")
elif(score>=60):
    print("D")
else:
    print("F")