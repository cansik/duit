from abc import ABC, abstractmethod
from typing import Any

from simbi.model.DataField import DataField


class BaseSerializer(ABC):

    @abstractmethod
    def handles_type(self, obj: Any) -> bool:
        pass

    @abstractmethod
    def serialize(self, obj: Any) -> [bool, Any]:
        pass
