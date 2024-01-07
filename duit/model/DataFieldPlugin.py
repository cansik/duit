from __future__ import annotations

from abc import ABC
from typing import TypeVar, Generic

import duit.model.DataField

T = TypeVar("T")


class DataFieldPlugin(ABC, Generic[T]):
    """
    An abstract base class for DataField plugins that can customize the behavior of DataField instances.
    """

    def __init__(self):
        """
        Initialize a DataFieldPlugin instance.
        """
        self.order_index: int = 0

    def on_register(self, field: duit.model.DataField.DataField[T]):
        """
        Called when the plugin is registered with a DataField instance.

        Args:
            field (duit.model.DataField.DataField[T]): The DataField instance that the plugin is registered with.
        """
        pass

    def on_unregister(self, field: duit.model.DataField.DataField[T]):
        """
        Called when the plugin is unregistered from a DataField instance.

        Args:
            field (duit.model.DataField.DataField[T]): The DataField instance that the plugin is unregistered from.
        """
        pass

    def on_set_value(self, field: duit.model.DataField.DataField[T], old_value: T, new_value: T) -> T:
        """
        Called when the value of the associated DataField is set.

        Args:
            field (duit.model.DataField.DataField[T]): The DataField instance with which the plugin is associated.
            old_value (T): The old value of the DataField.
            new_value (T): The new value to be set.

        Returns:
            T: The modified or unmodified new value.
        """
        return new_value

    def on_get_value(self, field: duit.model.DataField.DataField[T], value: T) -> T:
        """
        Called when the value of the associated DataField is retrieved.

        Args:
            field (duit.model.DataField.DataField[T]): The DataField instance with which the plugin is associated.
            value (T): The current value of the DataField.

        Returns:
            T: The modified or unmodified value.
        """
        return value

    def on_fire(self, field: duit.model.DataField.DataField[T], value: T) -> T:
        """
        Called when the 'on_changed' event of the associated DataField is fired.

        Args:
            field (duit.model.DataField.DataField[T]): The DataField instance with which the plugin is associated.
            value (T): The current value of the DataField.

        Returns:
            T: The modified or unmodified value.
        """
        return value
