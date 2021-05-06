n = int(input())
people = [int(input()) for _ in range(n)]


def crossing(people):
	if len(people) <= 2: return people[-1]
	
	

people.sort()
print(crossing(people))