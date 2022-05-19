from abc import ABC, abstractmethod

from duit.model.DataField import DataField


class Annotation(ABC):

    @abstractmethod
    def __ror__(self, model: DataField) -> DataField:
        pass
