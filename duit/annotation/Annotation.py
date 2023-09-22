from abc import ABC, abstractmethod
from typing import TypeVar

from duit.model.DataField import DataField

M = TypeVar("M", bound=DataField)


class Annotation(ABC):

    @abstractmethod
    def __ror__(self, model: M) -> M:
        pass

    @staticmethod
    @abstractmethod
    def _get_annotation_attribute_name() -> str:
        pass
