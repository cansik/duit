from pathlib import Path
from typing import Any, Type

from duit.settings.serialiser.BaseSerializer import BaseSerializer


class PathSerializer(BaseSerializer):
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
        return isinstance(obj, Path)

    def serialize(self, obj: Path) -> [bool, Any]:
        """
        Serialize a Path object by returning its string representation.

        Args:
            obj (Path): The Path object to be serialized.

        Returns:
            [bool, Any]: A tuple containing a success flag (True) and the string representation of the Path.

        Raises:
            None
        """
        return True, str(obj)

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
        return True, Path(obj)
