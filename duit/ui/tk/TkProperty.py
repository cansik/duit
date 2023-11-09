from abc import ABC
from typing import Generic, Optional

from duit.model.DataField import T
from duit.ui.BaseProperty import BaseProperty, M
from duit.ui.annotations import UIAnnotation


class TkProperty(Generic[T, M], BaseProperty[T, M], ABC):
    def __init__(self, annotation: UIAnnotation, model: Optional[M] = None):
        """
        Initializes a TkProperty.

        Args:
            annotation (UIAnnotation): The UI annotation associated with this property.
            model (Optional[M], optional): The model to link with the property. Defaults to None.
        """
        super().__init__(annotation, model)
