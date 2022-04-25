from enum import Enum, EnumMeta
from typing import Any, Type

from duit.settings.serialiser.BaseSerializer import BaseSerializer


class EnumSerializer(BaseSerializer):
    def handles_type(self, obj: Any) -> bool:
        return isinstance(obj, Enum)

    def serialize(self, obj: Enum) -> [bool, Any]:
        return True, obj.name

    def deserialize(self, data_type: EnumMeta, obj: Any) -> [bool, Any]:
        options = {o.name: o for o in list(data_type)}

        if obj not in options:
            return False, obj

        return True, options[obj]
