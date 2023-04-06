from abc import ABC
from typing import Generic, Optional

from duit.model.DataField import T, DataField
from duit.ui.BaseProperty import BaseProperty, M
from duit.ui.annotations import UIAnnotation


class TkProperty(Generic[T, M], BaseProperty[T, M], ABC):
    def __init__(self, annotation: UIAnnotation, model: Optional[M] = None):
        super().__init__(annotation, model)
