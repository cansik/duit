from __future__ import annotations

from typing import TypeVar, Generic, Any, Optional, Callable, Iterable, List, Sequence

import numpy as np

import duit.model.DataFieldPlugin
from duit.event.Event import Event
from duit.settings import SETTING_ANNOTATION_ATTRIBUTE_NAME

T = TypeVar("T")


class DataField(Generic[T]):
    """
    A generic data field that can hold a value of type T and provides event handling functionality.
    """

    def __init__(self, value: T):
        """
        Initialize a DataField with the given value.

        Args:
            value (T): The initial value of the DataField.
        """
        self._value: T = value
        self.publish_enabled: bool = True
        self.on_changed: Event[T] = Event[T]()
        self._plugins: List[duit.model.DataFieldPlugin.DataFieldPlugin] = []

        # Add serialization attribute by default
        from duit.settings.Setting import Setting
        self.__setattr__(SETTING_ANNOTATION_ATTRIBUTE_NAME, Setting())

    @property
    def value(self) -> T:
        """
        Get the current value of the DataField.

        Returns:
            T: The current value.
        """
        value = self._value

        if self._plugins:
            for plugin in self._plugins:
                value = plugin.on_get_value(self, value)

        return value

    @value.setter
    def value(self, new_value: T) -> None:
        """
        Set the value of the DataField and trigger the 'on_changed' event if the value changes.

        Args:
            new_value (T): The new value to set.
        """
        old_value = self._value

        if self._plugins:
            for plugin in reversed(self._plugins):
                new_value = plugin.on_set_value(self, old_value, new_value)

        self._value = new_value

        if self.publish_enabled and not self._is_equal(self._value, old_value):
            self.fire()

    def set(self, value: T) -> None:
        """
        Set the value of the DataField.

        Args:
            value (T): The new value to set.
        """
        self.value = value

    def set_silent(self, value: T) -> None:
        """
        Set the value of the DataField without triggering the 'on_changed' event.

        Args:
            value (T): The new value to set.
        """
        old_publish_value = self.publish_enabled
        self.publish_enabled = False
        self.value = value
        self.publish_enabled = old_publish_value

    def fire(self):
        """
        Trigger the 'on_changed' event with the current value.
        """
        value = self._value

        if self._plugins:
            for plugin in self._plugins:
                value = plugin.on_fire(self, value)

        self.on_changed(value)

    def fire_latest(self):
        """
        Trigger the 'on_changed' event with the current value, invoking only the latest listener.
        """
        self.on_changed.invoke_latest(self._value)

    def bind_to(self, model: "DataField[T]") -> None:
        """
        Bind this DataField to another DataField, propagating changes from this to the other.

        Args:
            model (DataField[T]): The target DataField to bind to.
        """

        def on_change(*args: Any):
            old_publish_value = self.publish_enabled
            self.publish_enabled = False
            model.value = self._value
            self.publish_enabled = old_publish_value

        self.on_changed.append(on_change)

    def bind_bidirectional(self, model: "DataField[T]") -> None:
        """
        Bind this DataField bidirectionally to another DataField.

        Args:
            model (DataField[T]): The target DataField to bind to bidirectionally.
        """
        self.bind_to(model)
        model.bind_to(self)

    def bind_to_attribute(self, obj: Any, field_name: Any,
                          converter: Optional[Callable[[T], Any]] = None,
                          fire_latest: bool = False) -> None:
        """
        Bind this DataField to an attribute of an object.

        Args:
            obj (Any): The target object.
            field_name (Any): The name of the attribute to bind to.
            converter (Optional[Callable[[T], Any]]): A converter function to apply to the value.
            fire_latest (bool): Whether to trigger the 'on_changed' event with the latest value.
        """

        def on_change(*args: Any):
            if hasattr(obj, field_name):
                output_value = self._value
                if converter is not None:
                    output_value = converter(output_value)

                setattr(obj, field_name, output_value)

        self.on_changed.append(on_change)

        if fire_latest:
            self.fire_latest()

    def register_plugin(self, *plugins: duit.model.DataFieldPlugin.DataFieldPlugin):
        """
        Register one or more DataField plugins with this DataField.

        Args:
            *plugins (duit.model.DataFieldPlugin.DataFieldPlugin): One or more DataField plugins to register.
        """
        self._plugins += plugins
        self._plugins = sorted(self._plugins, key=lambda x: x.order_index)
        for plugin in self._plugins:
            plugin.on_register(self)

    def unregister_plugin(self, *plugins: duit.model.DataFieldPlugin.DataFieldPlugin):
        """
        Unregister one or more DataField plugins from this DataField.

        Args:
            *plugins (duit.model.DataFieldPlugin.DataFieldPlugin): One or more DataField plugins to unregister.
        """
        for plugin in plugins:
            self._plugins.remove(plugin)
            plugin.on_unregister(self)

    def clear_plugins(self):
        """
        Clear all registered DataField plugins from this DataField.
        """
        self._plugins.clear()

    @property
    def plugins(self) -> Sequence[duit.model.DataFieldPlugin.DataFieldPlugin]:
        """
        Get the sequence of registered DataField plugins.

        Returns:
            Sequence[duit.model.DataFieldPlugin.DataFieldPlugin]: A sequence of DataField plugins.
        """
        return tuple(self._plugins)

    @staticmethod
    def _is_equal(value: T, new_value: T) -> bool:
        """
        Check if two values are equal, taking care of iterable comparisons (like numpy arrays).

        Args:
            value (T): The first value.
            new_value (T): The second value.

        Returns:
            bool: True if the values are equal, False otherwise.
        """
        if isinstance(value, np.ndarray):
            return np.array_equal(value, new_value)

        result = value == new_value

        # fix numpy and list comparisons
        if isinstance(result, Iterable):
            return all(result)

        return result

    def __repr__(self) -> str:
        return f"{type(self).__name__}[{type(self._value).__name__}] ({self._value})"

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other: object) -> bool:
        if isinstance(other, DataField):
            return self._is_equal(self.value, other.value)
        return False

    def __getstate__(self):
        d = dict(self.__dict__)
        # reset the event because handlers may not be pickled
        d["on_changed"] = Event()
        return d
