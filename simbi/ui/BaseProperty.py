from abc import ABC, abstractmethod
from typing import Optional, Any, Iterable

from simbi.model.DataModel import DataModel
from simbi.ui.annotations import UIAnnotation


class BaseProperty(ABC):
    def __init__(self, annotation: UIAnnotation, model: Optional[DataModel] = None):
        self.annotation = annotation
        self.model = model

    @abstractmethod
    def create_widgets(self) -> Iterable[Any]:
        pass
