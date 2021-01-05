import sys

def mix(solutions):
    answer=[0,0]

    if(solutions[-1] <= 0):answer[0]=solutions[-2]; answer[1] = solutions[-1]   # alkali 다 알칼리 용액일 때 -
    elif(solutions[0] >= 0):answer[0]=solutions[0]; answer[1] = solutions[1]    # acid 다 산성 용액일 떄 + 
    else:
        sol_sum   = 10**10 # abs value

        for i in range(len(solutions)):
            sol = solutions[i]
            pl = i+1                # 검색 범위의 맨 앞 원소 인덱스
            pr = len(solutions) - 1 # 검색 범위의 맨 끝 원소의 인덱스


            while True:
                pc = (pl+pr)//2     #중앙 원소의 인덱스
                
                if pc == i: break   # i가 가장 마지막 index이면 pl==pr==pc가 되므로 자기 자신을 검색하게 되므로 break
                if pl > pr: break
                else:
                    temp_sum = solutions[pc]+sol
                    if(abs(temp_sum) < sol_sum):
                        sol_sum = abs(temp_sum)
                        answer[0] = sol; answer[1] = solutions[pc]
                        
                    # Binary Search
                    if  temp_sum == 0: return answer   # 검색 성공
                    elif temp_sum < 0: pl = pc + 1     # 혼합 용액 값이 0보다 작으면 검색 범위를 뒤쪽 절반으로
                    else:              pr = pc - 1     # 혼합 용액 값이 0보다 크면 검색 범위를 앞쪽 절반으로          
           
    return answer

#### MAIN ####
# input 받아오는 부분
n = list(map(int, sys.stdin.readline().split()))[0]
solutions = list(map(int, sys.stdin.readline().split()))
solutions.sort()

ans = mix(solutions)
print(ans[0], ans[1])