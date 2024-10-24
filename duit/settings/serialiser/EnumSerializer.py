from enum import Enum, EnumMeta
from typing import Any

from duit.settings.serialiser.BaseSerializer import BaseSerializer


class EnumSerializer(BaseSerializer):
    """
    A serializer for Python Enum objects.

    Args:
        None
    """

    def handles_type(self, obj: Any) -> bool:
        """
        Check if the serializer can handle a given object.

        Args:
            obj (Any): The object to check.

        Returns:
            bool: True if the object is an instance of an Enum, otherwise False.
        """
        return isinstance(obj, Enum)

    def serialize(self, obj: Enum) -> [bool, Any]:
        """
        Serialize an Enum object by returning its name.

        Args:
            obj (Enum): The Enum object to be serialized.

        Returns:
            [bool, Any]: A tuple containing a success flag (True) and the name of the Enum.

        Raises:
            None
        """
        return True, obj.name

    def deserialize(self, data_type: EnumMeta, obj: Any) -> [bool, Any]:
        """
        Deserialize data into an Enum object.

        Args:
            data_type (EnumMeta): The Enum class type.
            obj (Any): The data to be deserialized (Enum name).

        Returns:
            [bool, Any]: A tuple containing a success flag (True) and the corresponding Enum object.

        Raises:
            None
        """
        options = {o.name: o for o in list(data_type)}

        if obj not in options:
            return False, obj

        return True, options[obj]
