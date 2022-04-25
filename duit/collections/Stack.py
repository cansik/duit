from typing import TypeVar, Generic

T = TypeVar("T")


class Stack(Generic[T]):
    def __init__(self):
        self.stack = []

    def push(self, value: T):
        self.stack.append(value)

    def peek(self) -> T:
        return self.stack[-1]

    def pop(self) -> T:
        return self.stack.pop()

    @property
    def is_empty(self) -> bool:
        return len(self.stack) == 0
