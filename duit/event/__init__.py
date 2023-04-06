import logging
from typing import Any, Optional, Callable, TypeVar

T = TypeVar("T")


def event_mapping(obj: Any, key: str, transform: Optional[Callable[[T], T]] = None) -> Callable[[Any], None]:
    if not hasattr(obj, key):
        logging.warning(f"Object {obj} does not have an attribute called {key}.")

    def _handler(value: Any):
        if not hasattr(obj, key):
            raise Exception(f"Object {obj} does not have an attribute called {key}.")

        if transform is not None:
            value = transform(value)

        setattr(obj, key, value)

    return _handler
