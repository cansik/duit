from typing import TypeVar, Generic

T = TypeVar("T")


class Stack(Generic[T]):
    """
    A generic stack data structure.

    Args:
        None
    """

    def __init__(self):
        """
        Initialize an empty stack.

        Args:
            None
        """
        self.stack = []

    def push(self, value: T):
        """
        Push a value onto the stack.

        Args:
            value (T): The value to be pushed onto the stack.

        Returns:
            None
        """
        self.stack.append(value)

    def peek(self) -> T:
        """
        Get the top element of the stack without removing it.

        Returns:
            T: The top element of the stack.

        Raises:
            IndexError: If the stack is empty.
        """
        return self.stack[-1]

    def pop(self) -> T:
        """
        Pop and return the top element of the stack.

        Returns:
            T: The top element of the stack.

        Raises:
            IndexError: If the stack is empty.
        """
        return self.stack.pop()

    @property
    def is_empty(self) -> bool:
        """
        Check if the stack is empty.

        Returns:
            bool: True if the stack is empty, False otherwise.
        """
        return len(self.stack) == 0
