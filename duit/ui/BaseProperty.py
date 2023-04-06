from abc import ABC, abstractmethod
from typing import Optional, Any, Iterable, TypeVar, Generic

from duit.model.DataField import DataField
from duit.ui.annotations import UIAnnotation

T = TypeVar("T", bound=UIAnnotation)
M = TypeVar("M", bound=DataField)


class BaseProperty(Generic[T, M], ABC):
    def __init__(self, annotation: T, model: Optional[M] = None):
        self.annotation = annotation
        self.model = model

    @abstractmethod
    def create_widgets(self) -> Iterable[Any]:
        pass
