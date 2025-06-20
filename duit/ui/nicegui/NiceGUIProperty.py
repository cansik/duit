from abc import ABC
from typing import Generic, Optional

from duit.model.DataField import T
from duit.ui.BaseProperty import BaseProperty, M
from duit.ui.annotations import UIAnnotation


class NiceGUIProperty(Generic[T, M], BaseProperty[T, M], ABC):
    """
    A generic property class for NiceGUI that extends BaseProperty.

    This class is designed to manage properties that are tied to UI annotations and models.
    """

    def __init__(self, annotation: UIAnnotation, model: Optional[M] = None):
        """
        Initializes a NiceGUIProperty.

        Args:
            annotation (UIAnnotation): The UI annotation associated with this property.
            model (Optional[M], optional): The model to link with the property. Defaults to None.
        """
        super().__init__(annotation, model)
