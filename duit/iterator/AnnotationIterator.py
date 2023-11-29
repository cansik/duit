from typing import TypeVar, Any

from duit.annotation.Annotation import Annotation
from duit.iterator.ObjectIterator import ObjectIterator

A = TypeVar("A", bound=Annotation)


class AnnotationIterator(ObjectIterator[A]):
    def __init__(self, obj: Any, recursive: bool = True, only_recurse_public_fields: bool = True):
        super().__init__(obj, Annotation, recursive, only_recurse_public_fields)
