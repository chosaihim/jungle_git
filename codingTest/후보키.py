from itertools import combinations

relation = [["100", "ryan"  ,"music"   ,"2"],
            ["200", "apeach","math"    ,"2"],
            ["300", "tube"  ,"computer","3"],
            ["400", "con"   ,"computer","4"],
            ["500", "muzi"  ,"music"   ,"3"],
            ["600", "apeach","music"   ,"2"]]

# uniqueness
# minimality

# find all combinations
def solution(relation):
    answer = 0
    
    key_set = []
    col_len = len(relation[0])
    row_len = len(relation)
    indices = [i for i in range(col_len)]
    index_comb = []
    
    # index combination
    for i in range(1, col_len+1):
        combi = combinations(indices,i)
        for comb in combi:
            comb_set = set()
            for c in comb:
                comb_set.add(c)
            index_comb.append(comb)
            
    # print(index_comb)
    
    #check uniqueness
    
    for comb in index_comb:
        # print(f'comb:{comb}')
        
        # make a trial key set with the combination
        trial = set()
        for row in range(row_len):
            onekey = ''
            for col in comb:
                onekey += relation[row][col]
            trial.add(onekey)
        # print(f'tiral:{trial}')
        
        validset_flag = True
        # 이거 총 row 개수와 같다면!!
        if(len(trial) == row_len):
            # print(f'enough entries: {trial}')
            # 이제 이 set의 subset이 존재하지 않는다면
            for key in key_set:
                if key.issubset(comb):
                    validset_flag = False
                    break
            # 추가해주기!
            if validset_flag:
                temp_set = set()
                for c in comb:
                    temp_set.add(c)
                key_set.append(temp_set)
            
        # print(key_set)

    answer = len(key_set)    
    return answer

print(solution(relation))