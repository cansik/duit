import base64
from pathlib import Path
from typing import Any, Type

import numpy as np

from duit.settings.serialiser.BaseSerializer import BaseSerializer

SHAPE_ATTRIBUTE = "shape"
DTYPE_ATTRIBUTE = "dtype"
DATA_ATTRIBUTE = "data"


class NumpySerializer(BaseSerializer):
    """
    A serializer for Python's pathlib.Path objects.

    Args:
        None
    """

    def handles_type(self, obj: Any) -> bool:
        """
        Check if the serializer can handle a given object.

        Args:
            obj (Any): The object to check.

        Returns:
            bool: True if the object is an instance of a pathlib.Path object, otherwise False.
        """
        return isinstance(obj, np.ndarray)

    def serialize(self, obj: np.ndarray) -> [bool, Any]:
        """
        Serialize a Path object by returning its string representation.

        Args:
            obj (Path): The Path object to be serialized.

        Returns:
            [bool, Any]: A tuple containing a success flag (True) and the string representation of the Path.

        Raises:
            None
        """
        data = {
            SHAPE_ATTRIBUTE: list(obj.shape),
            DTYPE_ATTRIBUTE: str(obj.dtype),
            DATA_ATTRIBUTE: base64.b64encode(obj.data.tobytes()).decode("utf-8")
        }
        return True, data

    def deserialize(self, data_type: Type, obj: Any) -> [bool, Any]:
        """
        Deserialize data into a pathlib.Path object.

        Args:
            data_type (Type): The expected data type for deserialization.
            obj (Any): The data to be deserialized (a string representing a Path).

        Returns:
            [bool, Any]: A tuple containing a success flag (True) and the corresponding pathlib.Path object.

        Raises:
            None
        """
        shape = tuple(obj[SHAPE_ATTRIBUTE])
        dtype = np.dtype(obj[DTYPE_ATTRIBUTE])

        data_bytes = str(obj[DATA_ATTRIBUTE]).encode("utf-8")
        buffer = base64.b64decode(data_bytes)
        data = np.frombuffer(buffer, dtype).reshape(shape)
        return True, data
