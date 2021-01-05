import sys
# debugFlag = True
debugFlag = False

def mix(solutions):
    answer=[0,0]

    # alkali 다 알칼리 용액일 때 -
    if(solutions[-1] <= 0):answer[0]=solutions[-2]; answer[1] = solutions[-1]
    # acid 다 산성 용액일 떄 +    
    elif(solutions[0] >= 0):answer[0]=solutions[0]; answer[1] = solutions[1]
    else:
        sol_sum   = 10**10 # abs value

        for i in range(len(solutions)):
            sol = solutions[i]
            if(debugFlag): print(f'i:{i}, solution: {sol}')

            pl = i+1                # 검색 범위의 맨 앞 원소 인덱스
            pr = len(solutions) - 1 # 검색 범위의 맨 끝 원소의 인덱스


            while True:
                pc = (pl+pr)//2     #중앙 원소의 인덱스
                
                if(debugFlag): print(f'pc:{pc}, solutions[pc]:{solutions[pc]} pl:{pl}, pr:{pr}')

                
                if pc == i: 
                    if(debugFlag): print(f'pc({pc}) == i({i})')
                    break

                temp_sum = solutions[pc]+sol
                if(abs(temp_sum) < sol_sum):
                    sol_sum = abs(temp_sum)
                    answer[0] = sol; answer[1] = solutions[pc]
                    
                if pl > pr:
                    break
                
                # Binary Search
                if temp_sum == 0:     #검색 성공
                    return answer
                elif temp_sum < 0:   
                    pl = pc + 1     # 검색 범위를 뒤쪽 절반으로
                else:               
                    pr = pc -1      # 검색 범위를 앞쪽 절반으로          
        
    return answer

#### MAIN ####
# input 받아오는 부분
n = list(map(int, sys.stdin.readline().split()))[0]
solutions = list(map(int, sys.stdin.readline().split()))
solutions.sort()

if debugFlag: print(f'n:{n}, solutions:{solutions}')

ans = mix(solutions)
print(ans[0], ans[1])
