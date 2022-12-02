from abc import ABC
from functools import total_ordering

from duit.annotation.Annotation import Annotation
from duit.model.DataField import DataField

UI_ANNOTATION_ATTRIBUTE_NAME = "__duit_ui_annotation"


@total_ordering
class UIAnnotation(Annotation, ABC):
    def __init__(self, name: str, tooltip: str = "", read_only: bool = False, importance: int = 10):
        self.name = name
        self.tooltip = tooltip
        self.read_only = read_only
        self._importance = importance

    def __ror__(self, model) -> DataField:
        if not isinstance(model, DataField):
            raise Exception(f"UIAnnotation can not be applied to {type(model).__name__}")

        # add ui attribute to data model
        if hasattr(model, UI_ANNOTATION_ATTRIBUTE_NAME):
            model.__getattribute__(UI_ANNOTATION_ATTRIBUTE_NAME).append(self)
        else:
            model.__setattr__(UI_ANNOTATION_ATTRIBUTE_NAME, [self])

        return model

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, UIAnnotation):
            return NotImplemented
        return self.name.lower() == other.name.lower()

    def __lt__(self, other):
        if not isinstance(other, UIAnnotation):
            return NotImplemented
        return self._importance < other._importance
