from typing import TypeVar, Generic, Callable, List

T = TypeVar('T')
H = Callable[[T], None]


class Event(Generic[T]):
    def __init__(self):
        self._handlers: List[H] = []

    def append(self, handler: H) -> None:
        self._handlers.append(handler)

    def invoke(self, value: T) -> None:
        for handler in self._handlers:
            handler(value)

    def invoke_latest(self, value: T) -> None:
        if len(self._handlers) == 0:
            return
        self._handlers[-1](value)

    def clear(self) -> None:
        self._handlers.clear()

    @property
    def handler_size(self) -> int:
        return len(self._handlers)

    def __iadd__(self, other):
        self.append(other)
        return self

    def __call__(self, value: T):
        self.invoke(value)
