from typing import List, Generic, Optional

from duit.model.DataField import DataField, T


class DataList(DataField[List[T]], Generic[T]):
    """
    A generic data field for managing a list of values of type T.
    """

    def __init__(self, values: Optional[List[T]] = None):
        """
        Initialize a DataList with optional initial values.

        Args:
            values (Optional[List[T]]): The initial values for the DataList. Defaults to an empty list if not provided.
        """
        if values is None:
            values = []

        super().__init__(values)

    def __len__(self) -> int:
        """
        Get the number of elements in the DataList.

        Returns:
            int: The number of elements in the list.
        """
        return len(self.value)

    def __getitem__(self, index: int) -> T:
        """
        Get the element at the specified index in the DataList.

        Args:
            index (int): The index of the element to retrieve.

        Returns:
            T: The element at the specified index.
        """
        return self.value[index]

    def __setitem__(self, index: int, value: T) -> None:
        """
        Set the element at the specified index in the DataList and trigger the 'on_changed' event.

        Args:
            index (int): The index of the element to set.
            value (T): The new value to set at the specified index.
        """
        self.value[index] = value
        self.fire()

    def __delitem__(self, index: int) -> None:
        """
        Delete the element at the specified index in the DataList and trigger the 'on_changed' event.

        Args:
            index (int): The index of the element to delete.
        """
        del self.value[index]
        self.fire()

    def insert(self, index: int, value: T) -> None:
        """
        Insert a value at the specified index in the DataList and trigger the 'on_changed' event.

        Args:
            index (int): The index at which to insert the value.
            value (T): The value to insert.
        """
        self.value.insert(index, value)
        self.fire()

    def append(self, value: T) -> None:
        """
        Append a value to the end of the DataList and trigger the 'on_changed' event.

        Args:
            value (T): The value to append.
        """
        self.value.append(value)
        self.fire()

    def extend(self, other: List[T]) -> None:
        """
        Extend the DataList with values from another list and trigger the 'on_changed' event.

        Args:
            other (List[T]): The list of values to extend with.
        """
        self.value.extend(other)
        self.fire()

    def pop(self, index: int = -1) -> T:
        """
        Remove and return the element at the specified index in the DataList and trigger the 'on_changed' event.

        Args:
            index (int): The index of the element to remove and return.

        Returns:
            T: The removed element.
        """
        value = self.value.pop(index)
        self.fire()
        return value

    def remove(self, value: T) -> None:
        """
        Remove the first occurrence of a value in the DataList and trigger the 'on_changed' event.

        Args:
            value (T): The value to remove.
        """
        self.value.remove(value)
        self.fire()

    def clear(self) -> None:
        """
        Remove all elements from the DataList and trigger the 'on_changed' event.
        """
        self.value.clear()
        self.fire()

    def index(self, value: T, start: int = 0, end: int = None) -> int:
        """
        Find the index of the first occurrence of a value within a specified range in the DataList.

        Args:
            value (T): The value to search for.
            start (int): The starting index for the search.
            end (int): The ending index for the search.

        Returns:
            int: The index of the first occurrence of the value within the specified range.
        """
        return self.value.index(value, start, end)

    def count(self, value: T) -> int:
        """
        Count the number of occurrences of a value in the DataList.

        Args:
            value (T): The value to count.

        Returns:
            int: The number of occurrences of the value in the list.
        """
        return self.value.count(value)

    def sort(self, key=None, reverse: bool = False) -> None:
        """
        Sort the elements in the DataList and trigger the 'on_changed' event.

        Args:
            key: A function to customize the sort order.
            reverse (bool): Whether to sort in reverse order.
        """
        self.value.sort(key=key, reverse=reverse)
        self.fire()

    def reverse(self) -> None:
        """
        Reverse the order of elements in the DataList and trigger the 'on_changed' event.
        """
        self.value.reverse()
        self.fire()

    def __iter__(self):
        """
        Initialize the iterator for iterating through the elements in the DataList.
        """
        self._iter_index = 0
        return self

    def __next__(self):
        """
        Get the next element in the DataList during iteration.

        Returns:
            T: The next element in the list.

        Raises:
            StopIteration: When all elements have been iterated.
        """
        if self._iter_index >= len(self):
            raise StopIteration
        result = self[self._iter_index]
        self._iter_index += 1
        return result

    def __repr__(self) -> str:
        return f"{type(self).__name__} {self._value}"

    def __str__(self):
        return self.__repr__()
