from typing import Generic, Optional, List

from duit.event.Event import Event
from duit.model.DataField import T
from duit.model.DataList import DataList


class SelectableDataList(DataList[T], Generic[T]):
    """
    A generic data list that supports selecting items with an associated index.
    """

    def __init__(self, values: Optional[List[T]] = None, selected_index: Optional[int] = None):
        """
        Initialize a SelectableDataList with optional initial values and a selected index.

        Args:
            values (Optional[List[T]]): The initial values for the SelectableDataList. Defaults to an empty list if not provided.
            selected_index (Optional[int]): The initial selected index. If not provided, it defaults to 0 if there are values.
        """
        if values is None:
            values = []

        super().__init__(values)

        if len(values) > 0:
            selected_index = 0

        self._selected_index = selected_index

        self.on_index_changed: Event[Optional[int]] = Event[Optional[int]]()

    @property
    def selected_index(self) -> Optional[int]:
        """
        Get the currently selected index in the SelectableDataList.

        Returns:
            Optional[int]: The selected index, or None if no item is selected.
        """
        return self._selected_index

    @selected_index.setter
    def selected_index(self, value: Optional[int]):
        """
        Set the selected index and trigger the 'on_index_changed' event if it changes.

        Args:
            value (Optional[int]): The index to select, or None to clear the selection.
        """
        old_value = self._selected_index
        self._selected_index = value

        if old_value != value:
            self.on_index_changed(value)

    @property
    def selected_item(self) -> Optional[T]:
        """
        Get the currently selected item in the SelectableDataList.

        Returns:
            Optional[T]: The selected item, or None if no item is selected.
        """
        if self._selected_index is None:
            return None

        return self[self._selected_index]

    @selected_item.setter
    def selected_item(self, value: T):
        """
        Set the selected item based on its value and trigger the 'on_index_changed' event.

        Args:
            value (T): The item to select.
        """
        self.selected_index = self.index(value)
