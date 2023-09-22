from typing import Optional, TypeVar

from duit.annotation.Annotation import Annotation
from duit.model.DataField import DataField
from duit.settings import SETTING_ANNOTATION_ATTRIBUTE_NAME

M = TypeVar("M", bound=DataField)


class Setting(Annotation):
    def __init__(self, name: Optional[str] = None, exposed: bool = True):
        self.name = name
        self.exposed = exposed

    def __ror__(self, model: M) -> M:
        if not isinstance(model, DataField):
            raise Exception(f"UIAnnotation can not be applied to {type(model).__name__}")

        # add ui attribute to data model
        model.__setattr__(SETTING_ANNOTATION_ATTRIBUTE_NAME, self)
        return model

    @staticmethod
    def _get_annotation_attribute_name() -> str:
        return SETTING_ANNOTATION_ATTRIBUTE_NAME
