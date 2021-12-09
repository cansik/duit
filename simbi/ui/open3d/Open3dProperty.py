from abc import ABC
from typing import Optional, Generic

from simbi.model.DataField import DataField
from simbi.ui.BaseProperty import BaseProperty, T
from simbi.ui.annotations import UIAnnotation


class Open3dProperty(Generic[T], BaseProperty[T], ABC):
    def __init__(self, annotation: UIAnnotation, model: Optional[DataField] = None):
        super().__init__(annotation, model)
