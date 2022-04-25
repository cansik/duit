from enum import Enum
from typing import Any

from simbi.settings.serialiser.BaseSerializer import BaseSerializer


class EnumSerializer(BaseSerializer):
    def handles_type(self, obj: Any) -> bool:
        return isinstance(obj, Enum)

    def serialize(self, obj: Enum) -> [bool, Any]:
        return True, obj.name
