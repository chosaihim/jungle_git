def solution(places):
    answer = []
    
    def is_safe(place, row, col):
        dr = [1,0,-1,0]
        dc = [0,1,0,-1]
        nr = [0,-1,0,1]
        nc = [1,0,-1,0]
        
        for d in range(4):
            r = row + dr[d]; c = col + dc[d]
            
            if 0 <= r < 5 and 0 <= c < 5:
                if place[r][c] == 'P':
                    return False
                elif place[r][c] == 'O':
                    
                    fr = r + dr[d]; fc = c +dc[d]
                    if 0 <= fr < 5 and 0 <= fc < 5 and place[fr][fc] == 'P':
                        return False
                    
                    rr = r + nr[d]; rc = c + nc[d]
                    if 0 <= rr < 5 and 0 <= rc < 5 and place[rr][rc] == 'P':
                        return False
                    
                    lr = r - nr[d]; lc = c - nc[d]
                    if 0 <= lr < 5 and 0 <= lc < 5 and place[lr][lc] == 'P':
                        return False        
                    
        return True

    
    for place_str in places:
        flag = True
        place = [list(p_str) for p_str in place_str]

        for i in range(5):
            for j in range(5):
                if place[i][j] == 'P':
                    if not is_safe(place,i,j):
                        flag = False
                        break
            if not flag: break
        
        if flag: answer.append(1)
        else: answer.append(0)
            
    
    return answer

places = [["POOOP", "OXXOX", "OPXPX", "OOXOX", "POXXP"], ["POOPX", "OXPXP", "PXXXO", "OXXXO", "OOOPP"], ["PXOPX", "OXOXP", "OXPXX", "OXXXP", "POOXX"], ["OOOXX", "XOOOX", "OOOXX", "OXOOX", "OOOOO"], ["PXPXP", "XPXPX", "PXPXP", "XPXPX", "PXPXP"]]
# places = [["PPOPX", "OXPXP", "PXXXO", "OXXXO", "OOOPP"]]
print(solution(places))
# [1, 0, 1, 1, 1]