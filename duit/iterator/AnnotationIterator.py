from typing import TypeVar, Any
from duit.annotation.Annotation import Annotation
from duit.iterator.ObjectIterator import ObjectIterator

A = TypeVar("A", bound=Annotation)


class AnnotationIterator(ObjectIterator[A]):
    """
    An iterator for iterating over objects with annotations.

    Args:
        obj (Any): The object to iterate over.
        recursive (bool, optional): If True, the iterator will recursively iterate over nested objects.
            Defaults to True.
        only_recurse_public_fields (bool, optional): If True, the iterator will only recurse into public fields.
            Defaults to True.
    """

    def __init__(self, obj: Any, recursive: bool = True, only_recurse_public_fields: bool = True):
        """
        Initialize the AnnotationIterator.

        Args:
            obj (Any): The object to iterate over.
            recursive (bool, optional): If True, the iterator will recursively iterate over nested objects.
                Defaults to True.
            only_recurse_public_fields (bool, optional): If True, the iterator will only recurse into public fields.
                Defaults to True.
        """
        super().__init__(obj, Annotation, recursive, only_recurse_public_fields)