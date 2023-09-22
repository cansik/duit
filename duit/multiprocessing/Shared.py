from typing import TypeVar

from duit.annotation.Annotation import Annotation
from duit.model.DataField import DataField
from duit.multiprocessing import MULTI_PROCESSING_ANNOTATION_ATTRIBUTE_NAME

M = TypeVar("M", bound=DataField)


class Shared(Annotation):
    def __init__(self):
        super().__init__()

    def __ror__(self, model: M) -> M:
        if not isinstance(model, DataField):
            raise Exception(f"Shared can not be applied to {type(model).__name__}")

        # add attribute to data model
        model.__setattr__(MULTI_PROCESSING_ANNOTATION_ATTRIBUTE_NAME, self)
        return model

    @staticmethod
    def _get_annotation_attribute_name() -> str:
        return MULTI_PROCESSING_ANNOTATION_ATTRIBUTE_NAME
