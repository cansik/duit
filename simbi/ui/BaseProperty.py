from abc import ABC, abstractmethod
from typing import Optional, Any, Iterable, TypeVar, Generic

from simbi.model.DataModel import DataModel
from simbi.ui.annotations import UIAnnotation

T = TypeVar("T", bound=UIAnnotation)


class BaseProperty(Generic[T], ABC):
    def __init__(self, annotation: T, model: Optional[DataModel] = None):
        self.annotation = annotation
        self.model = model

    @abstractmethod
    def create_widgets(self) -> Iterable[Any]:
        pass
