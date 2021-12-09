from abc import ABC
from typing import Optional

from simbi.model.DataModel import DataModel
from simbi.ui.BaseProperty import BaseProperty
from simbi.ui.annotations import UIAnnotation


class Open3dProperty(BaseProperty, ABC):
    def __init__(self, annotation: UIAnnotation, model: Optional[DataModel] = None):
        super().__init__(annotation, model)
