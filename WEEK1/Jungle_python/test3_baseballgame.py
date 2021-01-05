import sys
from itertools import permutations

debug_flag = True
n = list(map(int, sys.stdin.readline().split()))[0]

candidates = [i for i in range(102,1000)]
remove = []

for candi in candidates :

    f = candi//100 ; 
    s = (candi-f*100)//10; 
    t = candi %10
    
    if(f == 0 or s == 0 or t == 0): remove.append(candi); continue;
    elif(f == s): remove.append(candi); continue;
    elif(f == t): remove.append(candi); continue    
    elif(s == t): remove.append(candi); continue;
    elif(f == s == t): remove.append(candi); continue

for i in range(len(remove)):
    candidates.remove(remove[i])

remove.clear()

def isStrike(ans,trial):
    strike = 0
    
    f_ans  = ans//100 ; s_ans = (ans-f_ans*100)//10; t_ans  = ans %10
    f_try  = trial//100 ; s_try = (trial-f_try*100)//10; t_try  = trial %10

    if(f_ans == f_try): strike += 1
    if(s_ans == s_try): strike += 1
    if(t_ans == t_try): strike += 1

    return strike

def isBall(ans,trial):
    ball =0

    f_ans  = ans//100 ; s_ans = (ans-f_ans*100)//10; t_ans  = ans %10
    f_try  = trial//100 ; s_try = (trial-f_try*100)//10; t_try  = trial %10

    if(f_ans != f_try) and ((s_ans == f_try) or (t_ans == f_try)): ball += 1
    if(s_ans != s_try) and ((f_ans == s_try) or (t_ans == s_try)): ball += 1
    if(t_ans != t_try) and ((f_ans == t_try) or (s_ans == t_try)): ball += 1

    return ball

for i in range(n):
    trial, s, b = list(map(int, sys.stdin.readline().split())) # s: strike, b: ball

    for candi in candidates:
        if((isStrike(int(candi),trial) == s) and (isBall(int(candi),trial)==b)):
            continue
        else:
            remove.append(candi)
    
    for i in range(len(remove)):
        candidates.remove(remove[i])
    remove.clear()
        
print(len(candidates))