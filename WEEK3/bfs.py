korea = {'세종': set(['서울', '강릉', '대구', '광주']),
         '서울': set(['평양', '인천', '세종']),
         '강릉': set(['독도', '세종']),
         '광주': set(['세종', '여수']),
         '대구': set(['세종', '울산']),
         '평양': set(['서울', ]),
         '인천': set(['서울', ]),
         '독도': set(['강릉', ]),
         '여수': set(['광주', '부산']),
         '울산': set(['대구', '부산']),
         '부산': set(['여수', '울산']),
         }

def bfs(graph, root):
  visited = [] # 방문한 곳을 기록
  queue = [root] # 큐에 시작점을 줄세움
 
  while queue: # queue 가 빌 때 까지 탐색을 계속
    vertex = queue.pop(0) # 큐의 맨 앞의 원소를 방문할 꼭짓점으로 설정
 
    if vertex not in visited: # 꼭짓점이 방문된 적이 없다면 방문 기록에 추가
      visited.append(vertex)
      for node in graph[vertex]: # 꼭짓점에 연결된 노드들 중
        if node not in visited: # 방문 안 된 곳 만을
          queue.append(node) # 큐에 줄세움
 
  return visited
 
##### 실행결과 #####
print(bfs(korea, '세종'))