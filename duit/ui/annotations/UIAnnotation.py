from abc import ABC

from duit.annotation.Annotation import Annotation
from duit.model.DataField import DataField

UI_ANNOTATION_ATTRIBUTE_NAME = "__duit_ui_annotation"


class UIAnnotation(Annotation, ABC):
    def __init__(self, name: str, tooltip: str = "", read_only: bool = False):
        self.name = name
        self.tooltip = tooltip
        self.read_only = read_only

    def __ror__(self, model) -> DataField:
        if not isinstance(model, DataField):
            raise Exception(f"UIAnnotation can not be applied to {type(model).__name__}")

        # add ui attribute to data model
        if hasattr(model, UI_ANNOTATION_ATTRIBUTE_NAME):
            model.__getattribute__(UI_ANNOTATION_ATTRIBUTE_NAME).append(self)
        else:
            model.__setattr__(UI_ANNOTATION_ATTRIBUTE_NAME, [self])

        return model
