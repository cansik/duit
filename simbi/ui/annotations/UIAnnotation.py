from abc import ABC

from simbi.model.DataField import DataField

UI_ANNOTATION_ATTRIBUTE_NAME = "ui_annotation"


class UIAnnotation(ABC):
    def __init__(self, name: str):
        self.name = name

    def __ror__(self, model) -> DataField:
        if not isinstance(model, DataField):
            raise Exception(f"UIAnnotation can not be applied to {type(model).__name__}")

        # add ui attribute to data model
        if hasattr(model, UI_ANNOTATION_ATTRIBUTE_NAME):
            model.__getattribute__(UI_ANNOTATION_ATTRIBUTE_NAME).append(self)
        else:
            model.__setattr__(UI_ANNOTATION_ATTRIBUTE_NAME, [self])

        return model
