from typing import TypeVar, Generic, Any, Optional, Callable

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
        return self._value

    @value.setter
    def value(self, new_value: T) -> None:
        """
        Set the value of the DataField and trigger the 'on_changed' event if the value changes.

        Args:
            new_value (T): The new value to set.
        """
        old_value = self._value
        self._value = new_value

        if self.publish_enabled and not self._is_equal(self._value, old_value):
            self.fire()

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
        self.on_changed(self._value)

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

    @staticmethod
    def _is_equal(value: T, new_value: T) -> bool:
        """
        Check if two values are equal, taking care of iterable comparisons.

        Args:
            value (T): The first value.
            new_value (T): The second value.

        Returns:
            bool: True if the values are equal, False otherwise.
        """
        result = value == new_value

        # fix numpy and list comparisons
        if hasattr(result, '__iter__'):
            return all(result)

        return result

    def __repr__(self) -> str:
        return f"{type(self).__name__}[{type(self._value).__name__}] ({self._value})"

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other: object) -> bool:
        if isinstance(other, DataField):
            return self._is_equal_method(self.value, other.value)
        return False

    def __getstate__(self):
        d = dict(self.__dict__)
        del d["on_changed"]
        return d
