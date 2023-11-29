from dataclasses import dataclass
from typing import TypeVar, Any, Generic, List, Iterator, Type, Optional

OT = TypeVar("OT", bound=Any)


@dataclass
class ObjectIteratorResult(Generic[OT]):
    parent_field_name: Optional[str]
    parent: Any

    field_name: str
    field_value: OT


class ObjectIterator(Generic[OT]):
    def __init__(self, obj: Any, object_type: Type[OT],
                 recursive: bool = True, only_recurse_public_fields: bool = True):
        self._object_type = object_type
        self._recursive = recursive
        self.only_recurse_public_fields = only_recurse_public_fields

        self._results: List[ObjectIteratorResult] = []

        self._processed_objects = set()
        self._find_objects(obj)

    def __iter__(self) -> Iterator[ObjectIteratorResult]:
        return iter(self._results)

    def _find_objects(self, obj: Any, parent_field_name: Optional[str] = None):
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
        return hasattr(obj, "__dict__")
