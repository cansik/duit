from abc import ABC
from typing import Optional, Generic

from duit.model.DataField import DataField
from duit.ui.BaseProperty import BaseProperty, T, M
from duit.ui.annotations import UIAnnotation


class Open3dProperty(Generic[T, M], BaseProperty[T, M], ABC):
    def __init__(self, annotation: UIAnnotation, model: Optional[M] = None):
        super().__init__(annotation, model)
