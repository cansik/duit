from dataclasses import dataclass
from typing import TypeVar, Any, Generic, List, Iterator, Type, Optional

OT = TypeVar("OT", bound=Any)


@dataclass
class ObjectIteratorResult(Generic[OT]):
    """
    Represents a result of iterating over an object.

    Attributes:
        parent_field_name (Optional[str]): The name of the field in the parent object.
        parent (Any): The parent object.
        field_name (str): The name of the field in the parent object containing the result.
        field_value (OT): The value of the field.
    """
    parent_field_name: Optional[str]
    parent: Any
    field_name: str
    field_value: OT


class ObjectIterator(Generic[OT]):
    """
    An iterator for recursively iterating over an object's fields.

    Args:
        obj (Any): The object to iterate over.
        object_type (Type[OT]): The type of objects to look for during iteration.
        recursive (bool, optional): If True, the iterator will recursively iterate over nested objects.
            Defaults to True.
        only_recurse_public_fields (bool, optional): If True, the iterator will only recurse into public fields.
            Defaults to True.
    """

    def __init__(self, obj: Any, object_type: Type[OT],
                 recursive: bool = True, only_recurse_public_fields: bool = True):
        """
        Initialize the ObjectIterator.

        Args:
            obj (Any): The object to iterate over.
            object_type (Type[OT]): The type of objects to look for during iteration.
            recursive (bool, optional): If True, the iterator will recursively iterate over nested objects.
                Defaults to True.
            only_recurse_public_fields (bool, optional): If True, the iterator will only recurse into public fields.
                Defaults to True.
        """
        self._object_type = object_type
        self._recursive = recursive
        self.only_recurse_public_fields = only_recurse_public_fields

        self._results: List[ObjectIteratorResult] = []

        self._processed_objects = set()
        self._find_objects(obj)

    def __iter__(self) -> Iterator[ObjectIteratorResult]:
        """
        Returns an iterator for the results of the object iteration.

        Returns:
            Iterator[ObjectIteratorResult]: Iterator for the results of the object iteration.
        """
        return iter(self._results)

    def _find_objects(self, obj: Any, parent_field_name: Optional[str] = None):
        """
        Recursively finds objects of the specified type in the given object.

        Args:
            obj (Any): The object to search for objects of the specified type.
            parent_field_name (Optional[str]): The name of the field in the parent object.
        """
        self._processed_objects.add(id(obj))

        if not self._is_iterable(obj):
            return

        for name, value in obj.__dict__.items():
            if isinstance(value, self._object_type):
                self._results.append(ObjectIteratorResult(parent_field_name, obj, name, value))

            if self._recursive and id(value) not in self._processed_objects:
                if self.only_recurse_public_fields and name.startswith("_"):
                    continue
                self._find_objects(value, name)

    @staticmethod
    def _is_iterable(obj: Any) -> bool:
        """
        Checks if the given object is iterable.

        Args:
            obj (Any): The object to check.

        Returns:
            bool: True if the object is iterable, False otherwise.
        """
        return hasattr(obj, "__dict__")