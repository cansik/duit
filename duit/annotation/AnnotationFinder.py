from typing import Any, Dict, Tuple, TypeVar, Generic, Callable, Optional, Type

from duit.annotation.Annotation import Annotation
from duit.model.DataField import DataField

A = TypeVar("A", bound=Annotation)


class AnnotationFinder(Generic[A]):
    """
    AnnotationFinder is a generic class for finding annotations in objects.

    Args:
        annotation_type (Type[A]): The type of annotation to search for.
        is_field_valid (Optional[Callable[[DataField, A], bool]]): A function to determine if a DataField is valid for the given annotation (optional).
        recursive (bool): Whether to recursively search for annotations in nested objects (default is False).

    Attributes:
        annotation_type (Type[A]): The type of annotation to search for.
        is_field_valid (Optional[Callable[[DataField, A], bool]]): A function to determine if a DataField is valid for the given annotation (optional).
        recursive (bool): Whether to recursively search for annotations in nested objects.
    """

    def __init__(self, annotation_type: Type[A],
                 is_field_valid: Optional[Callable[[DataField, A], bool]] = None,
                 recursive: bool = False):
        """
        Initialize an AnnotationFinder instance.

        Args:
            annotation_type (Type[A]): The type of annotation to search for.
            is_field_valid (Optional[Callable[[DataField, A], bool]]): A function to determine if a DataField is valid for the given annotation (optional).
            recursive (bool): Whether to recursively search for annotations in nested objects (default is False).
        """
        self.annotation_type = annotation_type
        self.is_field_valid = is_field_valid
        self.recursive = recursive

        self._annotation_attribute_name = self.annotation_type._get_annotation_attribute_name()
        self._processed_objects = set()

    def find(self, obj: Any) -> Dict[str, Tuple[DataField, A]]:
        """
        Find annotations of the specified type in an object.

        Args:
            obj (Any): The object to search for annotations.

        Returns:
            Dict[str, Tuple[DataField, A]]: A dictionary of found annotations, where the keys are attribute names and values are tuples of DataField and the annotation.
        """
        self._processed_objects.clear()
        return self._find_all_annotations(obj)

    def _find_all_annotations(self, obj: Any) -> Dict[str, Tuple[DataField, A]]:
        """
        Recursively find all annotations in an object.

        Args:
            obj (Any): The object to search for annotations.

        Returns:
            Dict[str, Tuple[DataField, A]]: A dictionary of found annotations, where the keys are attribute names and values are tuples of DataField and the annotation.
        """
        annotations = {}
        self._processed_objects.add(id(obj))

        if not hasattr(obj, "__dict__"):
            return annotations

        for n, v in obj.__dict__.items():
            if isinstance(v, DataField):
                if hasattr(v, self._annotation_attribute_name):
                    a = v.__getattribute__(self._annotation_attribute_name)
                    if self.is_field_valid is not None and not self.is_field_valid(v, a):
                        continue
                    annotations[n] = (v, a)
                else:
                    value = v.value
                    if self.recursive and id(value) not in self._processed_objects:
                        annotations.update(self._find_all_annotations(value))
        return annotations
