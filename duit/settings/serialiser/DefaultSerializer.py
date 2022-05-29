from typing import Any, Type

from duit.settings.serialiser.BaseSerializer import BaseSerializer


class DefaultSerializer(BaseSerializer):
    def handles_type(self, obj: Any) -> bool:
        return True

    def serialize(self, obj: Any) -> [bool, Any]:
        return True, obj

    def deserialize(self, data_type: Type, obj: Any) -> [bool, Any]:
        return True, obj
