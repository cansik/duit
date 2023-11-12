from typing import Optional, TypeVar

from duit.annotation.Annotation import Annotation
from duit.model.DataField import DataField
from duit.settings import SETTING_ANNOTATION_ATTRIBUTE_NAME

M = TypeVar("M", bound=DataField)


class Setting(Annotation):
    """
    An annotation for marking data fields as settings.

    Args:
        name (Optional[str]): The name of the setting. If not provided, the field name is used.
        exposed (bool): Whether the setting should be exposed in the user interface. Default is True.
    """

    def __init__(self, name: Optional[str] = None, exposed: bool = True):
        """
        Initialize a Setting annotation.

        Args:
            name (Optional[str]): The name of the setting. If not provided, the field name is used.
            exposed (bool): Whether the setting should be exposed in the user interface. Default is True.
        """
        self.name = name
        self.exposed = exposed

    def _apply_annotation(self, model: M) -> M:
        """
        Apply the Setting annotation to a DataField model.

        Args:
            model (M): The DataField model to which the annotation is applied.

        Returns:
            M: The annotated DataField model.
        
        Raises:
            Exception: If the annotation is applied to a non-DataField model.
        """
        if not isinstance(model, DataField):
            raise Exception(f"UIAnnotation can not be applied to {type(model).__name__}")

        # add ui attribute to data model
        model.__setattr__(SETTING_ANNOTATION_ATTRIBUTE_NAME, self)
        return model

    @staticmethod
    def _get_annotation_attribute_name() -> str:
        """
        Get the attribute name used to store Setting annotations in DataField objects.

        Returns:
            str: The attribute name for storing Setting annotations.
        """
        return SETTING_ANNOTATION_ATTRIBUTE_NAME
