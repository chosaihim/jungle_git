import sys
input = sys.stdin.readline

vacation, busy = map(int, input().split())
busydays = list(map(int, input().split()))

# 하루 이용권	 10,000원 	 없음
# 연속 3일권	25,000원	쿠폰 1장
# 연속 5일권	37,000원	쿠폰 2장

dp = [[0 for coupon in range(2)] for day in range(vacation+1+5)]

for day in range(vacation+1):
    
    for coupon in range(3):
        
    
    
    
    # if day in busydays:
    #     for coupon in range(3):
    #         dp[day][coupon] = dp[day-1][coupon]
    
    # else: 
            
    #     for coupon in range(3):
    #         # 1일권
    #         dp[day][coupon] = dp[day-1][coupon] + 10000
    #         # 3일권
    #         if coupon == 0:
    #             dp[day][coupon] = min(dp[day][coupon], dp[day-4][2]+25000, dp[day-3][2]+25000)
    #         else: dp[day][coupon] = min(dp[day][coupon], dp[day-3][coupon-1]+25000)
    #         # 5일권
    #         if coupon == 0:
    #             dp[day][coupon] = min(dp[day][coupon], dp[day-6][1]+37000, dp[day-5][1]+37000)
    #         if coupon == 1:
    #             dp[day][coupon] = min(dp[day][coupon], dp[day-6][2]+37000, dp[day-5][2]+37000)
    #         else: dp[day][coupon] = min(dp[day][coupon], dp[day-3][coupon-1]+37000)
    
    print(dp)