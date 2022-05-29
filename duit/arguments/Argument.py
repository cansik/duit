from typing import Optional

from duit.annotation.Annotation import Annotation
from duit.arguments import ARGUMENT_ANNOTATION_ATTRIBUTE_NAME
from duit.model.DataField import DataField


class Argument(Annotation):
    def __init__(self, dest: Optional[str] = None, *args, group: Optional[str] = None,
                 auto_params: bool = True, **kwargs):
        self.dest = dest
        self.group = group
        self.args = args
        self.kwargs = kwargs
        self.auto_params = auto_params

    def __ror__(self, model) -> DataField:
        if not isinstance(model, DataField):
            raise Exception(f"UIAnnotation can not be applied to {type(model).__name__}")

        # read model parameter
        if self.auto_params:
            if "type" not in self.kwargs:
                self.kwargs["type"] = type(model.value)

            if "default" not in self.kwargs:
                self.kwargs["default"] = model.value

        # add ui attribute to data model
        model.__setattr__(ARGUMENT_ANNOTATION_ATTRIBUTE_NAME, self)
        return model
