from typing import Generic, Optional, List

from duit.event.Event import Event
from duit.model.DataField import T
from duit.model.DataList import DataList


class SelectableDataList(DataList[T], Generic[T]):
    def __init__(self, values: Optional[List[T]] = None, selected_index: Optional[int] = None):
        if values is None:
            values = []

        super().__init__(values)

        if len(values) > 0:
            selected_index = 0

        self._selected_index = selected_index

        self.on_index_changed: Event[Optional[int]] = Event[Optional[int]]()

    @property
    def selected_index(self) -> Optional[int]:
        return self._selected_index

    @selected_index.setter
    def selected_index(self, value: Optional[int]):
        old_value = self._selected_index
        self._selected_index = value

        if old_value != value:
            self.on_index_changed(value)

    @property
    def selected_item(self) -> Optional[T]:
        if self._selected_index is None:
            return None

        return self[self._selected_index]

    @selected_item.setter
    def selected_item(self, value: T):
        self.selected_index = self.index(value)
