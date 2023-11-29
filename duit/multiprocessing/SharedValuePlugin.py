import multiprocessing as mp
from typing import Any

from duit.model.DataField import DataField
from duit.model.DataFieldPlugin import DataFieldPlugin


class SharedValuePlugin(DataFieldPlugin):

    def __init__(self, shared_value: mp.Value):
        self.shared_value = shared_value

    def on_set_value(self, field: DataField[Any], old_value: Any, new_value: Any) -> Any:
        self.shared_value.value = new_value
        return new_value

    def on_get_value(self, field: DataField[Any], value: Any) -> Any:
        return self.shared_value.value

    def on_fire(self, field: DataField[Any], value: Any) -> Any:
        return self.shared_value.value
