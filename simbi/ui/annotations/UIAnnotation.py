from abc import ABC

from simbi.model.DataModel import DataModel

UI_ANNOTATION_ATTRIBUTE_NAME = "ui_annotation"


class UIAnnotation(ABC):
    def __init__(self, name: str):
        self.name = name

    def __ror__(self, model) -> DataModel:
        if not isinstance(model, DataModel):
            raise Exception(f"UIAnnotation can not be applied to {type(model).__name__}")

        # add ui attribute to data model
        if hasattr(model, UI_ANNOTATION_ATTRIBUTE_NAME):
            model.__getattribute__(UI_ANNOTATION_ATTRIBUTE_NAME).append(self)
        else:
            model.__setattr__(UI_ANNOTATION_ATTRIBUTE_NAME, [self])

        return model
