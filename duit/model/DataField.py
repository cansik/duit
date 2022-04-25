from typing import TypeVar, Generic

from duit.event.Event import Event
from duit.settings import SETTING_ANNOTATION_ATTRIBUTE_NAME

T = TypeVar('T')


class DataField(Generic[T]):
    def __init__(self, value: T):
        self._value: T = value
        self.publish_enabled: bool = True
        self.on_changed: Event[T] = Event[T]()

        # add serialization attribute by default
        from duit.settings.Setting import Setting
        self.__setattr__(SETTING_ANNOTATION_ATTRIBUTE_NAME, Setting())

    @property
    def value(self) -> T:
        return self._value

    @value.setter
    def value(self, new_value: T) -> None:
        old_value = self._value
        self._value = new_value

        if self.publish_enabled and self._value != old_value:
            self.fire()

    def set_silent(self, value: T) -> None:
        old_publish_value = self.publish_enabled
        self.publish_enabled = False
        self.value = value
        self.publish_enabled = old_publish_value

    def fire(self):
        self.on_changed(self._value)

    def fire_latest(self):
        self.on_changed.invoke_latest(self._value)

    def bind_to(self, model: "DataField[T]") -> None:
        def on_change():
            old_publish_value = self.publish_enabled
            self.publish_enabled = False
            model.value = self._value
            self.publish_enabled = old_publish_value

        self.on_changed.append(on_change)

    def bind_bidirectional(self, model: "DataField[T]") -> None:
        self.bind_to(model)
        model.bind_to(self)

    def __repr__(self) -> str:
        return f"DataModel[{type(self._value).__name__}] ({self._value})"

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other: object) -> bool:
        if isinstance(other, DataField):
            return self.value == other.value
        return False
