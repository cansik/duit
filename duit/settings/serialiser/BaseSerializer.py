from abc import ABC, abstractmethod
from typing import Any, Type


class BaseSerializer(ABC):
    """
    An abstract base class for serializers.

    Args:
        None
    """

    @abstractmethod
    def handles_type(self, obj: Any) -> bool:
        """
        Check if the serializer can handle a given object.

        Args:
            obj (Any): The object to check.

        Returns:
            bool: True if the serializer can handle the object, False otherwise.
        """
        pass

    @abstractmethod
    def serialize(self, obj: Any) -> [bool, Any]:
        """
        Serialize an object into a format suitable for storage.

        Args:
            obj (Any): The object to be serialized.

        Returns:
            [bool, Any]: A tuple containing a success flag (True if serialization is successful, False otherwise)
            and the serialized data.

        Raises:
            Exception: If serialization fails.
        """
        pass

    @abstractmethod
    def deserialize(self, data_type: Type, obj: Any) -> [bool, Any]:
        """
        Deserialize data into a specific type of object.

        Args:
            data_type (Type): The expected data type for deserialization.
            obj (Any): The data to be deserialized.

        Returns:
            [bool, Any]: A tuple containing a success flag (True if deserialization is successful, False otherwise)
            and the deserialized object.

        Raises:
            Exception: If deserialization fails.
        """
        pass
