from typing import List, Generic, Optional

from duit.model.DataField import DataField, T


class DataList(DataField[List[T]], Generic[T]):
    def __init__(self, values: Optional[List[T]] = None):
        if values is None:
            values = []

        super().__init__(values)

    def __len__(self) -> int:
        return len(self.value)

    def __getitem__(self, index: int) -> T:
        return self.value[index]

    def __setitem__(self, index: int, value: T) -> None:
        self.value[index] = value
        self.fire()

    def __delitem__(self, index: int) -> None:
        del self.value[index]
        self.fire()

    def insert(self, index: int, value: T) -> None:
        self.value.insert(index, value)
        self.fire()

    def append(self, value: T) -> None:
        self.value.append(value)
        self.fire()

    def extend(self, other: List[T]) -> None:
        self.value.extend(other)
        self.fire()

    def pop(self, index: int = -1) -> T:
        value = self.value.pop(index)
        self.fire()
        return value

    def remove(self, value: T) -> None:
        self.value.remove(value)
        self.fire()

    def clear(self) -> None:
        self.value.clear()
        self.fire()

    def index(self, value: T, start: int = 0, end: int = None) -> int:
        return self.value.index(value, start, end)

    def count(self, value: T) -> int:
        return self.value.count(value)

    def sort(self, key=None, reverse: bool = False) -> None:
        self.value.sort(key=key, reverse=reverse)
        self.fire()

    def reverse(self) -> None:
        self.value.reverse()
        self.fire()

    def __iter__(self):
        self._iter_index = 0
        return self

    def __next__(self):
        if self._iter_index >= len(self):
            raise StopIteration
        result = self[self._iter_index]
        self._iter_index += 1
        return result

    def __repr__(self) -> str:
        return f"{type(self).__name__} {self._value}"

    def __str__(self):
        return self.__repr__()
