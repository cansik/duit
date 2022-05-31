from abc import ABC
from typing import Generic, Optional

from duit.model.DataField import T, DataField
from duit.ui.BaseProperty import BaseProperty
from duit.ui.annotations import UIAnnotation


class TkProperty(Generic[T], BaseProperty[T], ABC):
    def __init__(self, annotation: UIAnnotation, model: Optional[DataField] = None):
        super().__init__(annotation, model)
