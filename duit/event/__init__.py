import logging
from typing import Any, Optional, Callable, TypeVar

T = TypeVar("T")


def event_mapping(obj: Any, key: str, transform: Optional[Callable[[T], T]] = None) -> Callable[[Any], None]:
    """
    Create and return an event handler that maps the value to the specified object attribute.

    Args:
        obj (Any): The target object.
        key (str): The name of the attribute in the target object where the value will be stored.
        transform (Optional[Callable[[T], T]]): An optional function to transform the incoming value before storing it.

    Returns:
        Callable[[Any], None]: An event handler function that can be used to set the object attribute with the incoming value.
    """
    if not hasattr(obj, key):
        logging.warning(f"Object {obj} does not have an attribute called {key}.")

    def _handler(value: Any):
        """
        Handle an incoming value by setting it to the specified object attribute.

        Args:
            value (Any): The value to be stored in the object attribute.
        """
        if not hasattr(obj, key):
            raise Exception(f"Object {obj} does not have an attribute called {key}.")

        if transform is not None:
            value = transform(value)

        setattr(obj, key, value)

    return _handler
