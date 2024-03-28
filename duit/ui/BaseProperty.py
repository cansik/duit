from abc import ABC, abstractmethod
from typing import Optional, Any, Iterable, TypeVar, Generic

from duit.model.DataField import DataField
from duit.ui.annotations import UIAnnotation

T = TypeVar("T", bound=UIAnnotation)
M = TypeVar("M", bound=DataField)


class BaseProperty(Generic[T, M], ABC):
    def __init__(self, annotation: T, model: Optional[M] = None):
        """
        Initialize a BaseProperty.

        :param annotation: The UIAnnotation associated with this property.
        :param model: An optional DataField model associated with the property.
        """
        self.annotation = annotation
        self.model = model

    @abstractmethod
    def create_widgets(self, *args) -> Iterable[Any]:
        """
        Create and return widgets for the property.

        This method should be implemented by subclasses to define the specific
        widgets that make up the property. The widgets can be of any type.

        :return: An iterable of widgets representing the property.
        """
        pass
