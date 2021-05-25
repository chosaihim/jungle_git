import sys
sys.setrecursionlimit(10**6)

def solution(U, L, C):
    C = [0] + C
    answer = []
    upper_row = []
    lower_row = []

    def dfs(U, L, upper, lower, col):
        ret = False

        upper_row.append(upper)
        lower_row.append(lower)

        if col == len(C):
            if sum(upper_row) == U and sum(lower_row) == L:
                
                for one in upper_row[2:]:
                    answer.append(str(one))
                answer.append(",")
                for one in lower_row[2:]:
                    answer.append(str(one))
                return True

        else:
            if C[col] == 2:
                ret = dfs(U, L, 1, 1, col+1)
            elif C[col] == 0:
                ret = dfs(U, L, 0, 0, col+1)
            else:
                ret = dfs(U, L, 1, 0, col+1)
                ret = dfs(U, L, 0, 1, col+1)
        
        upper_row.pop()
        lower_row.pop()

        return ret


    dfs(U, L, 0, 0, 0)
    if not answer:
        return "IMPOSSIBLE"
    else:
        answer_str = "".join(answer)
        return answer_str

