import multiprocessing as mp
from typing import Optional, Any

from duit.iterator.DataFieldIterator import DataFieldIterator
from duit.model.DataField import DataField
from duit.multiprocessing.SharedValuePlugin import SharedValuePlugin


class SharedContext:
    def __init__(self, manager: Optional[mp.Manager] = None):
        self.manager = mp.Manager() if manager is None else manager

        # add thread which is listening for events (in a shared queue)

    def share(self, obj: Any):
        for fields in DataFieldIterator(obj):
            field: DataField = fields.field_value
            self.share_field(field)

    def share_field(self, field: DataField):
        value = field.value
        value_type = type(value)

        shared_value: mp.Value = self.manager.Value(value_type, value)
        field.register_plugin(SharedValuePlugin(shared_value))
