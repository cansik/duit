import threading
from typing import Generic, Callable, List, Optional, Iterator, ParamSpec, Any, Dict, Tuple

P = ParamSpec("P")
PARAM_TYPE = Tuple[Tuple[Any, ...], Dict[str, Any]]
H = Callable[P, None]


class Event(Generic[P]):
    """
    A generic event class that allows you to register and trigger event handlers,
    and also provides a way to wait for the next event to be fired.

    Attributes:
        _handlers (List[H]): A list to store event handlers.
        _latest_value (Optional[PARAM_TYPE]): Stores the most recent event parameters.
        _event_trigger (threading.Event): A threading event to synchronize event waiting.
    """

    def __init__(self):
        """
        Initializes the Event instance with an empty list of handlers,
        an optional storage for the latest event parameters, and a threading event.
        """
        self._handlers: List[H] = []
        self._latest_value: Optional[PARAM_TYPE] = None
        self._event_trigger = threading.Event()

    def append(self, handler: H) -> None:
        """
        Appends an event handler to the list of handlers.

        Args:
            handler (H): The event handler function to add.
        """
        self._handlers.append(handler)

    def remove(self, handler: H) -> None:
        """
        Removes an event handler from the list of handlers.

        Args:
            handler (H): The event handler function to remove.
        """
        self._handlers.remove(handler)

    def contains(self, handler: H) -> bool:
        """
        Checks if a specific event handler is already registered.

        Args:
            handler (H): The event handler function to check.

        Returns:
            bool: True if the handler is registered, False otherwise.
        """
        return handler in self._handlers

    def invoke(self, *args: P.args, **kwargs: P.kwargs) -> None:
        """
        Invokes all registered event handlers with the provided arguments.
        Also sets the threading event to allow waiting mechanisms to proceed.

        Args:
            *args (P.args): Positional arguments to pass to the event handlers.
            **kwargs (P.kwargs): Keyword arguments to pass to the event handlers.
        """
        self._latest_value = (args, kwargs)
        for handler in self._handlers:
            handler(*args, **kwargs)

        # Trigger the event for waiting threads
        self._event_trigger.set()

    def invoke_latest(self, *args: P.args, **kwargs: P.kwargs) -> None:
        """
        Invokes the most recently added event handler with the provided arguments.

        If no event handlers are registered, this method does nothing.

        Args:
            *args (P.args): Positional arguments to pass to the latest event handler.
            **kwargs (P.kwargs): Keyword arguments to pass to the latest event handler.
        """
        if len(self._handlers) == 0:
            return
        self._handlers[-1](*args, **kwargs)

    def clear(self) -> None:
        """
        Clears all registered event handlers, removing them from the list.
        """
        self._handlers.clear()

    def register(self, handler: H) -> H:
        """
        Registers an event handler by appending it to the list.
        This method is intended for use as a decorator.

        Args:
            handler (H): The event handler function to add.

        Returns:
            H: The registered handler function.
        """
        self.append(handler)
        return handler

    @property
    def handler_size(self) -> int:
        """
        Returns the number of registered event handlers.

        Returns:
            int: The count of registered event handlers.
        """
        return len(self._handlers)

    def __iadd__(self, other: H) -> "Event[P]":
        """
        Enables the use of the `+=` operator to add an event handler.

        Args:
            other (H): The event handler function to add.

        Returns:
            Event[P]: The updated Event instance.
        """
        self.append(other)
        return self

    def __isub__(self, other: H) -> "Event[P]":
        """
        Enables the use of the `-=` operator to remove an event handler.

        Args:
            other (H): The event handler function to remove.

        Returns:
            Event[P]: The updated Event instance.
        """
        self.remove(other)
        return self

    def __contains__(self, item: H) -> bool:
        """
        Checks if a specific event handler is registered using the `in` operator.

        Args:
            item (H): The event handler function to check.

        Returns:
            bool: True if the handler is registered, False otherwise.
        """
        return self.contains(item)

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> None:
        """
        Allows the Event instance to be called as a function, invoking all registered handlers.

        Args:
            *args (P.args): Positional arguments to pass to the event handlers.
            **kwargs (P.kwargs): Keyword arguments to pass to the event handlers.
        """
        self.invoke(*args, **kwargs)

    def wait(self, timeout: Optional[float] = None) -> Optional[PARAM_TYPE]:
        """
        Waits for the next event to be fired, with an optional timeout.

        Args:
            timeout (Optional[float]): The maximum time (in seconds) to wait.
                                       If None, waits indefinitely.

        Returns:
            Optional[PARAM_TYPE]: The arguments passed when the event was triggered,
                                  or None if the timeout was reached.
        """
        event_occurred = self._event_trigger.wait(timeout)

        # If the event occurred, clear the event and return the latest value
        if event_occurred:
            self._event_trigger.clear()
            return self._latest_value
        else:
            return None

    def stream(self, timeout: Optional[float] = None) -> Iterator[Optional[PARAM_TYPE]]:
        """
        Continuously yields the event parameters whenever the event is triggered,
        with an optional timeout.

        Args:
            timeout (Optional[float]): The maximum time (in seconds) to wait
                                       between yielding values. If None, waits indefinitely.

        Yields:
            Optional[PARAM_TYPE]: The arguments passed each time the event is triggered,
                                  or None if the timeout was reached.
        """
        while True:
            yield self.wait(timeout)

    def __getstate__(self) -> Dict[str, Any]:
        """
        Custom method to remove the `_event_trigger` attribute from the state when pickling.

        Returns:
            Dict[str, Any]: The object's state dictionary excluding `_event_trigger`.
        """
        state = self.__dict__.copy()
        state["_event_trigger"] = None  # Exclude the event trigger from pickling
        return state

    def __setstate__(self, state: Dict[str, Any]) -> None:
        """
        Custom method to restore the `_event_trigger` attribute after unpickling.

        Args:
            state (Dict[str, Any]): The object's state dictionary.
        """
        self.__dict__.update(state)
        self._event_trigger = threading.Event()  # Reinitialize the event
