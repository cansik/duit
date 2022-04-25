from abc import ABC, abstractmethod
from typing import Any, Type

from duit.model.DataField import DataField


class BaseSerializer(ABC):

    @abstractmethod
    def handles_type(self, obj: Any) -> bool:
        pass

    @abstractmethod
    def serialize(self, obj: Any) -> [bool, Any]:
        pass

    @abstractmethod
    def deserialize(self, data_type: Type, obj: Any) -> [bool, Any]:
        pass
