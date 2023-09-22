from multiprocessing import Manager

from duit.model.DataField import DataField, T


class SharedDataField(DataField[T]):
    def __init__(self, value: T, manager: Manager):
        super().__init__(value)
        self._shared_value = manager.Value(type(value).__name__, value)

    @property
    def value(self) -> T:
        return self._shared_value.value

    @value.setter
    def value(self, new_value: T) -> None:
        old_value = self._shared_value.value
        self._shared_value.value = new_value

        if self.publish_enabled and not self._is_equal(new_value, old_value):
            self.fire()
