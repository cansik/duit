from typing import Any, Type

from duit.settings.serialiser.BaseSerializer import BaseSerializer


class DefaultSerializer(BaseSerializer):
    """
    A default serializer that handles any object type.

    Args:
        None
    """

    def handles_type(self, obj: Any) -> bool:
        """
        Check if the serializer can handle a given object.

        Args:
            obj (Any): The object to check.

        Returns:
            bool: True, as this serializer handles any object type.
        """
        return True

    def serialize(self, obj: Any) -> [bool, Any]:
        """
        Serialize an object into a format suitable for storage.

        Args:
            obj (Any): The object to be serialized.

        Returns:
            [bool, Any]: A tuple containing a success flag (True) and the serialized object (the same as the input object).

        Raises:
            None
        """
        return True, obj

    def deserialize(self, data_type: Type, obj: Any) -> [bool, Any]:
        """
        Deserialize data into a specific type of object.

        Args:
            data_type (Type): The expected data type for deserialization.
            obj (Any): The data to be deserialized.

        Returns:
            [bool, Any]: A tuple containing a success flag (True) and the deserialized object (the same as the input object).

        Raises:
            None
        """
        return True, obj
