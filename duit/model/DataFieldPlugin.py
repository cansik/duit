from __future__ import annotations

from abc import ABC
from typing import TypeVar, Generic

import duit.model.DataField

T = TypeVar("T")


class DataFieldPlugin(ABC, Generic[T]):

    def __init__(self):
        self.order_index: int = 0

    def on_register(self, field: duit.model.DataField.DataField[T]):
        pass

    def on_unregister(self, field: duit.model.DataField.DataField[T]):
        pass

    def on_set_value(self, field: duit.model.DataField.DataField[T], old_value: T, new_value: T) -> T:
        return new_value

    def on_get_value(self, field: duit.model.DataField.DataField[T], value: T) -> T:
        return value

    def on_fire(self, field: duit.model.DataField.DataField[T], value: T) -> T:
        return value
