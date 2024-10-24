from typing import Any

import vector

from duit.settings.serialiser.BaseSerializer import BaseSerializer
from duit.utils import _vector


class VectorSerializer(BaseSerializer):
    """
    A serializer for the `vector` library's Vector objects.

    Args:
        None
    """

    def handles_type(self, obj: Any) -> bool:
        """
        Check if the serializer can handle a given object.

        Args:
            obj (Any): The object to check.

        Returns:
            bool: True if the object is an instance of a `vector.Vector`, otherwise False.
        """
        return isinstance(obj, vector.Vector)

    def serialize(self, obj: vector.Vector) -> [bool, Any]:
        """
        Serialize a `vector.Vector` object by extracting its components.

        Args:
            obj (vector.Vector): The `vector.Vector` object to be serialized.

        Returns:
            [bool, Any]: A tuple containing a success flag (True) and a dictionary with the components of the vector.

        Raises:
            None
        """
        components = _vector.get_vector_attributes(obj)
        result = {c: getattr(obj, c) for c in components}
        return True, result

    def deserialize(self, data_type: type, obj: Any) -> [bool, Any]:
        """
        Deserialize data into a specific type of `vector.Vector` object.

        Args:
            data_type (type): The expected data type for deserialization (e.g., vector.Vector2D, vector.Vector3D).
            obj (Any): The data to be deserialized.

        Returns:
            [bool, Any]: A tuple containing a success flag (True) and the corresponding `vector.Vector` object.

        Raises:
            None
        """
        if issubclass(data_type, vector.Vector2D):
            return True, vector.obj(x=obj["x"], y=obj["y"])
        elif issubclass(data_type, vector.Vector3D):
            return True, vector.obj(x=obj["x"], y=obj["y"], z=obj["z"])
        elif issubclass(data_type, vector.Vector4D):
            return True, vector.obj(x=obj["x"], y=obj["y"], z=obj["z"], t=obj["t"])
        else:
            return False, None
