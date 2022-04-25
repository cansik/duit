from typing import Any

from simbi.settings.serialiser.BaseSerializer import BaseSerializer


class DefaultSerializer(BaseSerializer):
    def handles_type(self, obj: Any) -> bool:
        return False

    def serialize(self, obj: Any) -> [bool, Any]:
        return True, obj
