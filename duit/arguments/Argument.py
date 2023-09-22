from typing import Optional, TypeVar

from duit.annotation.Annotation import Annotation
from duit.arguments import ARGUMENT_ANNOTATION_ATTRIBUTE_NAME
from duit.model.DataField import DataField

M = TypeVar("M", bound=DataField)


class Argument(Annotation):

    def __init__(self, dest: Optional[str] = None, *args, group: Optional[str] = None,
                 auto_params: bool = True, **kwargs):
        self.dest = dest
        self.group = group
        self.args = args
        self.kwargs = kwargs
        self.auto_params = auto_params

    def __ror__(self, model: M) -> M:
        if not isinstance(model, DataField):
            raise Exception(f"Argument can not be applied to {type(model).__name__}")

        # read model parameter
        if self.auto_params:
            if "type" not in self.kwargs:
                self.kwargs["type"] = type(model.value)

            if "default" not in self.kwargs:
                self.kwargs["default"] = model.value

        # add ui attribute to data model
        model.__setattr__(ARGUMENT_ANNOTATION_ATTRIBUTE_NAME, self)
        return model

    @staticmethod
    def _get_annotation_attribute_name() -> str:
        return ARGUMENT_ANNOTATION_ATTRIBUTE_NAME
