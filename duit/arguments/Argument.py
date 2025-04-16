from typing import Optional, TypeVar

from duit.annotation.Annotation import Annotation
from duit.arguments import ARGUMENT_ANNOTATION_ATTRIBUTE_NAME
from duit.model.DataField import DataField

M = TypeVar("M", bound=DataField)


class Argument(Annotation):
    """
    Annotation class for defining command-line arguments.

    Args:
        dest (Optional[str]): The destination name for the argument (optional).
        group (Optional[str]): The argument group name (optional).
        auto_params (bool): Whether to automatically infer type and default values from the DataField (default is True).
        *args: Variable positional arguments.
        **kwargs: Variable keyword arguments.

    Attributes:
        dest (Optional[str]): The destination name for the argument.
        group (Optional[str]): The argument group name.
        args: Variable positional arguments.
        kwargs: Variable keyword arguments.
        auto_params (bool): Whether to automatically infer type and default values from the DataField.
    """

    def __init__(self, dest: Optional[str] = None, *args, group: Optional[str] = None,
                 auto_params: bool = True, auto_default: bool = False, allow_none: bool = False, **kwargs):
        """
        Initialize an Argument instance.

        Args:
            dest (Optional[str]): The destination name for the argument (optional).
            group (Optional[str]): The argument group name (optional).
            auto_params (bool): Whether to automatically infer type and other values from the DataField (default is True).
            auto_default (bool): Whether to automatically infer default value from the DataField (default is False).
            allow_none (bool): Whether to allow None as valid value. Otherwise, it is evaluated as not set.
            *args: Variable positional arguments.
            **kwargs: Variable keyword arguments.
        """
        self.dest = dest
        self.group = group
        self.args = args
        self.kwargs = kwargs
        self.auto_params = auto_params
        self.auto_default = auto_default
        self.allow_none = allow_none

    def _apply_annotation(self, model: M) -> M:
        """
        Apply the Argument annotation to a DataField model.

        Args:
            model (M): The DataField model to apply the Argument to.

        Returns:
            M: The modified DataField model with the Argument applied.
        """
        if not isinstance(model, DataField):
            raise Exception(f"Argument can not be applied to {type(model).__name__}")

        # read model parameter
        if self.auto_params:
            if "type" not in self.kwargs:
                self.kwargs["type"] = type(model.value)

        if self.auto_default:
            if "default" not in self.kwargs:
                self.kwargs["default"] = model.value

        # add ui attribute to data model
        model.__setattr__(ARGUMENT_ANNOTATION_ATTRIBUTE_NAME, self)
        return model

    @staticmethod
    def _get_annotation_attribute_name() -> str:
        """
        Get the name of the annotation attribute.

        Returns:
            str: The name of the annotation attribute (used for Argument).
        """
        return ARGUMENT_ANNOTATION_ATTRIBUTE_NAME
