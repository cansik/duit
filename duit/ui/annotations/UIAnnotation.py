from abc import ABC
from functools import total_ordering
from typing import TypeVar

from duit.annotation.Annotation import Annotation
from duit.model.DataField import DataField

UI_ANNOTATION_ATTRIBUTE_NAME = "__duit_ui_annotation"

T = TypeVar('T', bound=DataField)


@total_ordering
class UIAnnotation(Annotation, ABC):
    def __init__(self, name: str, tooltip: str = "", read_only: bool = False, importance: int = 10):
        """
        Initialize a UIAnnotation.

        :param name: The name of the UI annotation.
        :param tooltip: The tooltip text for the annotation.
        :param read_only: Whether the annotation is read-only (default is False).
        :param importance: The importance level of the annotation (default is 10).
        """
        self.name = name
        self.tooltip = tooltip
        self.read_only = read_only
        self._importance = importance

    def _apply_annotation(self, model: T) -> T:
        """
        Add the UI annotation to a data model.

        :param model: The data model to which the UI annotation is applied.
        :return: The data model with the UI annotation added.
        """
        if not isinstance(model, DataField):
            raise Exception(f"UIAnnotation can not be applied to {type(model).__name__}")

        # add ui attribute to data model
        if hasattr(model, UI_ANNOTATION_ATTRIBUTE_NAME):
            model.__getattribute__(UI_ANNOTATION_ATTRIBUTE_NAME).append(self)
        else:
            model.__setattr__(UI_ANNOTATION_ATTRIBUTE_NAME, [self])

        return model

    def __eq__(self, other: object) -> bool:
        """
        Check if two UI annotations are equal.

        :param other: The other UI annotation to compare.
        :return: True if the annotations have the same name (case-insensitive), otherwise False.
        """
        if not isinstance(other, UIAnnotation):
            return NotImplemented
        return self.name.lower() == other.name.lower()

    def __lt__(self, other):
        """
        Compare two UI annotations based on their importance levels.

        :param other: The other UI annotation to compare.
        :return: True if this annotation's importance is less than the other's, otherwise False.
        """
        if not isinstance(other, UIAnnotation):
            return NotImplemented
        return self._importance < other._importance

    @staticmethod
    def _get_annotation_attribute_name() -> str:
        """
        Get the name of the attribute used to store UI annotations in a data model.

        :return: The name of the attribute used to store UI annotations.
        """
        return UI_ANNOTATION_ATTRIBUTE_NAME
