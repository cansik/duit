from typing import TypeVar, Any
from duit.iterator.ObjectIterator import ObjectIterator
from duit.model.DataField import DataField

DF = TypeVar("DF", bound=DataField)


class DataFieldIterator(ObjectIterator[DF]):
    """
    An iterator for iterating over objects with data fields.

    Args:
        obj (Any): The object to iterate over.
        recursive (bool, optional): If True, the iterator will recursively iterate over nested objects.
            Defaults to True.
        only_recurse_public_fields (bool, optional): If True, the iterator will only recurse into public fields.
            Defaults to True.
    """

    def __init__(self, obj: Any, recursive: bool = True, only_recurse_public_fields: bool = True):
        """
        Initialize the DataFieldIterator.

        Args:
            obj (Any): The object to iterate over.
            recursive (bool, optional): If True, the iterator will recursively iterate over nested objects.
                Defaults to True.
            only_recurse_public_fields (bool, optional): If True, the iterator will only recurse into public fields.
                Defaults to True.
        """
        super().__init__(obj, DataField, recursive, only_recurse_public_fields)