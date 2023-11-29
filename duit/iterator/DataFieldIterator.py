from typing import TypeVar, Any

from duit.iterator.ObjectIterator import ObjectIterator
from duit.model.DataField import DataField

DF = TypeVar("DF", bound=DataField)


class DataFieldIterator(ObjectIterator[DF]):
    def __init__(self, obj: Any, recursive: bool = True, only_recurse_public_fields: bool = True):
        super().__init__(obj, DataField, recursive, only_recurse_public_fields)
