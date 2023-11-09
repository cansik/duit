from typing import TypeVar, Generic, Callable, List

T = TypeVar('T')
H = Callable[[T], None]


class Event(Generic[T]):
    """
    A generic event class that allows you to register and trigger event handlers.

    Attributes:
        _handlers (List[H]): A list to store event handlers.
    """

    def __init__(self):
        """
        Initialize the Event instance with an empty list of handlers.
        """
        self._handlers: List[H] = []

    def append(self, handler: H) -> None:
        """
        Append an event handler to the list of handlers.

        Args:
            handler (H): The event handler function to add.
        """
        self._handlers.append(handler)

    def remove(self, handler: H) -> None:
        """
        Remove an event handler from the list of handlers.

        Args:
            handler (H): The event handler function to remove.
        """
        self._handlers.remove(handler)

    def contains(self, handler: H) -> bool:
        """
        Check if a specific event handler is already registered.

        Args:
            handler (H): The event handler function to check for.

        Returns:
            bool: True if the handler is in the list, False otherwise.
        """
        return handler in self._handlers

    def invoke(self, value: T) -> None:
        """
        Invoke all registered event handlers with the provided value.

        Args:
            value (T): The value to pass to the event handlers.
        """
        for handler in self._handlers:
            handler(value)

    def invoke_latest(self, value: T) -> None:
        """
        Invoke the most recently added event handler with the provided value.

        If no event handlers are registered, this method does nothing.

        Args:
            value (T): The value to pass to the latest event handler.
        """
        if len(self._handlers) == 0:
            return
        self._handlers[-1](value)

    def clear(self) -> None:
        """
        Clear all registered event handlers, removing them from the list.
        """
        self._handlers.clear()

    @property
    def handler_size(self) -> int:
        """
        Get the number of registered event handlers.

        Returns:
            int: The number of event handlers currently registered.
        """
        return len(self._handlers)

    def __iadd__(self, other):
        """
        Allow the use of '+=' to add an event handler.

        Args:
            other (H): The event handler function to add.

        Returns:
            Event[T]: The updated Event instance.
        """
        self.append(other)
        return self

    def __isub__(self, other):
        """
        Allow the use of '-=' to remove an event handler.

        Args:
            other (H): The event handler function to remove.

        Returns:
            Event[T]: The updated Event instance.
        """
        self.remove(other)
        return self

    def __contains__(self, item) -> bool:
        """
        Check if a specific event handler is already registered using 'in' operator.

        Args:
            item (H): The event handler function to check for.

        Returns:
            bool: True if the handler is in the list, False otherwise.
        """
        return self.contains(item)

    def __call__(self, value: T):
        """
        Allow the instance to be called as a function, invoking all event handlers.

        Args:
            value (T): The value to pass to the event handlers.
        """
        self.invoke(value)
