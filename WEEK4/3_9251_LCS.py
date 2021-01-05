import sys
input = sys.stdin.readline

# input
str1_string = " " + input()
str2_string = " " + input()
str1 = list(str1_string)
str2 = list(str2_string)
# print(f'str1:{str1}, str2:{str2}')

dp = [[0] * (len(str1)-1) for i in range(len(str2)-1)]


for row in range(1, len(str2)-1):
    for col in range(1, len(str1)-1):
        
        
        # print(f'str1[col]:{str1[col]}, str2[row]:{str2[row]}')
        
        dp[row][col] = max(dp[row][col-1], dp[row-1][col]) 

        temp = dp[row][col]
        if(str2[row] == str1[col]):
            dp[row][col] = dp[row-1][col-1] + 1
            dp[row][col] = max(dp[row][col],temp)

# for i in range(len(str2)-1):
#     print(dp[i])        

print(dp[len(str2)-2][len(str1)-2])
