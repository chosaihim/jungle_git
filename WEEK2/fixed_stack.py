from typing import Any


class FixedStack:
    #고정 길이 스택 클래스

    class Empty(Exception):
        pass

    class Full(Exception):
        pass

    def __init__(self, capcity: int = 256) -> None:
        self.stk = [None]* capcity  #스택 본체
        self.capacity = capacity    # stack size
        self.ptr = 0                # stack pointer
    
    def __len__(self) -> int:
        return self.ptr
    
    def is_empty(self) -> bool:
        return self.ptr <= 0

    def is_full(self) -> bool:
        return self.ptr >= self.capacity
    
    def push(self, value:Any) -> None:
        if self.is_full():
            raise FixedStack.Full
        self.stk[self.ptr] = value
        self.ptr += 1
    
    def pop(self) -> Any:
        if self.is_empty():
            raise FixedStack.Empty
        self.ptr -= 1
        return self.stk[self.ptr]
    
    def peek(self) -> Any:
        if self.is_empty():
            raise FixedStack.Empty
        return self.stk[self.ptr-1]
    
    def clear(self) -> None: #스택을 비움. 모든 데이터 삭제
        self.ptr = 0

    def find(self, value:Any) -> Any:
        for i in range(self.ptr -1, -1, -1):
            if self.stk[i] == value:
                return i
            return -1               # 검색 실패
    
    def count(self, value:Any)-> bool:
        c = 0
        for i in range(self.ptr):   # scan from bottom to top. 선형검색
            if self.stk[i] == value:
                c += 1
        return c
    
    def __contains__(self, value:Any)->bool:
        return self.count(value)
    
    def dump(self) -> None:
        if self.is_empty():
            print('스택이 비어 있습니다.')
        else:
            print(self.stk[:self.ptr])
