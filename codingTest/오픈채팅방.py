import sys
input = sys.stdin.readline

def solution(record):
    answer = []
    nickNames = {}
    actionStr = {"Enter":"님이 들어왔습니다.", "Leave":"님이 나갔습니다."}
    
    for r in record:
        splited = r.split()
        if splited[0] != "Leave":
            nickNames[splited[1]] = splited[2]
            
            
    for r in record:
        splited = r.split()
        if splited[0] != "Change":
            answer.append(nickNames[splited[1]] + actionStr[splited[0]])
    
    return answer