import threading
from abc import ABC, abstractmethod
from contextlib import contextmanager
from functools import wraps
from typing import Optional, Any, Iterable, TypeVar, Generic

from duit.model.DataField import DataField
from duit.ui.annotations import UIAnnotation

T = TypeVar("T", bound=UIAnnotation)
M = TypeVar("M", bound=DataField)


class BaseProperty(Generic[T, M], ABC):
    """
    Abstract base class representing a generic property with an associated UI annotation and data model.

    This class provides the structure for managing UI-bound properties with optional underlying models.
    It supports thread-safe operations and requires implementation of a widget creation method.

    :param annotation: The UIAnnotation associated with this property.
    :param model: An optional DataField model associated with the property.
    """

    def __init__(self, annotation: T, model: Optional[M] = None):
        """
        Initialize a BaseProperty.

        :param annotation: The UIAnnotation associated with this property.
        :param model: An optional DataField model associated with the property.
        """
        self.annotation = annotation
        self.model = model

        self._silent_lock = threading.Lock()

    @abstractmethod
    def create_widgets(self, *args) -> Iterable[Any]:
        """
        Create and return widgets for the property.

        This method should be implemented by subclasses to define the specific
        widgets that make up the property. The widgets can be of any type.

        :returns: An iterable of widgets representing the property.
        """
        pass

    @contextmanager
    def silent(self):
        """
        Context manager to temporarily suppress updates or notifications.

        This is useful for batching operations where intermediate updates are not needed.
        Ensures thread-safe entry and exit using a non-blocking lock.

        :yields: True if the lock was acquired and operations are silent, otherwise False.
        """
        acquired = self._silent_lock.acquire(blocking=False)
        if not acquired:
            yield False
            return
        try:
            yield True
        finally:
            self._silent_lock.release()

    @staticmethod
    def suppress_updates(method):
        """
        Decorator to wrap callbacks in a silent() context,
        whether they’re bound methods or nested functions capturing `self`.
        """

        @wraps(method)
        def wrapper(*args, **kwargs):
            # Check if it's a bound method: args[0] is the instance
            instance = None
            if args and hasattr(args[0], "silent"):
                instance = args[0]
            else:
                # Otherwise, look in the function closure for 'self'
                closure = getattr(method, "__closure__", None)
                if closure:
                    names = method.__code__.co_freevars
                    for idx, name in enumerate(names):
                        if name == "self":
                            instance = closure[idx].cell_contents
                            break

            # If no BaseProperty instance found, just call through
            if instance is None:
                return method(*args, **kwargs)

            # Otherwise run inside the silent lock
            with instance.silent() as ok:
                if not ok:
                    return
                return method(*args, **kwargs)

        return wrapper
