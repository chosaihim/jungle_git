from typing import Any

class FixedQueue:
    
    class Empty(Exception):
        pass
    
    class Full(Exception):
        pass

    def __init__(self, capacity:int) -> None:
        self.no = 0                 # 현재 데이터 개수
        self.front = 0              # 맨 앞 원소 커서
        self.rear = 0               # 맨 끝 원소 커서
        self.capacity = capacity    # 큐의 크기
        self.que = [None]*capacity  # 큐의 본체

    def __len__(self) -> int:
        return self.no
    
    def is_empty(self) -> bool:
        return self.no <= 0
    
    def is_full(self) -> bool:
        return self.no >= self.capacity
    
    def enque(self, x:Any) -> None:
        if self.is_full():
            raise FixedQueue.Full

        self.que[self.rear] = x
        self.rear += 1
        self.no   += 1
        if self.rear == self.capacity:
            self.rear = 0
    
    def deque(self) -> Any:
        if self.is_empty():
            raise FixedQueue.Empty
        
        x = self.que[self.front]
        self.front += 1
        self.no    -= 1
        if self.front == self.capacity:
            self.front = 0
        return x