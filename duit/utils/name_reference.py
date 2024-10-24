from typing import Generic, TypeVar

T = TypeVar("T")


class NameReferenceDecorator(Generic[T]):
    """
    A generic decorator class that returns the name of an attribute when accessed.

    Args:
        T: The type of the object being decorated.
        
    Attributes:
        obj (T): The object being decorated.
    """

    def __init__(self, obj: T):
        """
        Initialize the decorator with the object to be decorated.

        Args:
            obj (T): The object to be decorated.
        """
        self.obj = obj

    def __getattribute__(self, item) -> str:
        """
        Get the name of an attribute when it is accessed.

        Args:
            item (str): The name of the attribute.

        Returns:
            str: The name of the attribute.

        Raises:
            None
        """

        return item


def create_name_reference(obj: T) -> T:
    """
    Create a name reference decorator for an object.

    Args:
        obj (T): The object to create a name reference for.

    Returns:
        T: The decorated object with name reference functionality.

    Raises:
        None
    """
    decorator = NameReferenceDecorator(obj)
    return decorator
