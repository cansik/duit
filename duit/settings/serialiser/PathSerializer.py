from pathlib import Path
from typing import Any, Type

from duit.settings.serialiser.BaseSerializer import BaseSerializer


class PathSerializer(BaseSerializer):
    def handles_type(self, obj: Any) -> bool:
        return isinstance(obj, Path)

    def serialize(self, obj: Path) -> [bool, Any]:
        return True, str(obj)

    def deserialize(self, data_type: Type, obj: Any) -> [bool, Any]:
        return True, Path(obj)
