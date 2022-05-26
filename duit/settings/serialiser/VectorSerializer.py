from enum import EnumMeta
from typing import Any

import vector

from duit.settings.serialiser.BaseSerializer import BaseSerializer
from duit.utils import _vector


class VectorSerializer(BaseSerializer):
    def handles_type(self, obj: Any) -> bool:
        return isinstance(obj, vector.Vector)

    def serialize(self, obj: vector.Vector) -> [bool, Any]:
        components = _vector.get_vector_attributes(obj)
        result = {c: getattr(obj, c) for c in components}
        return True, result

    def deserialize(self, data_type: type, obj: Any) -> [bool, Any]:
        if issubclass(data_type, vector.Vector2D):
            return True, vector.obj(x=obj["x"], y=obj["y"])
        elif issubclass(data_type, vector.Vector3D):
            return True, vector.obj(x=obj["x"], y=obj["y"], z=obj["z"])
        elif issubclass(data_type, vector.Vector4D):
            return True, vector.obj(x=obj["x"], y=obj["y"], z=obj["z"], t=obj["t"])
        else:
            return False, None
