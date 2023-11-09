from typing import List, Callable, Optional

from open3d.cpu.pybind.visualization import gui


class SelectionBox(gui.Vert):
    def __init__(self, *args, **kwargs):
        """
        Constructor for SelectionBox class.

        This class represents a user interface widget that combines a preview text, open button, and a list view for selecting items.

        """
        super().__init__(*args, **kwargs)

        self.list_size: int = 200

        self._preview_text = gui.TextEdit()
        self._preview_text.enabled = False

        self._open_button = gui.Button("¬")
        self._open_button.vertical_padding_em = 0
        self._open_button.horizontal_padding_em = 0
        self._open_button.set_on_clicked(self._on_button_clicked)

        self._list = gui.ListView()
        self._list.set_on_selection_changed(self._on_list_selection_changed)

        self._list_panel = gui.StackedWidget()
        self._list_panel.visible = False
        self._list_panel.background_color = gui.Color(1.0, 0.0, 0.0, 1.0)
        self._list_panel.add_child(self._list)

        container = gui.Horiz(4)
        container.add_child(self._preview_text)
        container.add_child(self._open_button)

        self.add_child(container)
        self.add_child(self._list_panel)

        self._on_selection_changed_handler: Optional[Callable[[str, int], None]] = None

        self._items: List[str] = []

        self.background_color = gui.Color(255, 0, 0, 1)

    def _on_button_clicked(self):
        """
        Handle the button click event to show/hide the list.

        This method is called when the open button is clicked and toggles the visibility of the list.

        """
        rect: gui.Rect = self.frame
        self._list_panel.frame = gui.Rect(rect.x, rect.y + rect.height, rect.width, self.list_size)
        self._list.frame = gui.Rect(rect.x, rect.y + rect.height, rect.width, self.list_size)
        self._list_panel.visible = not self._list_panel.visible

    def _on_list_selection_changed(self, new_val, is_double_click):
        """
        Handle the list selection change event.

        Args:
            new_val (str): The new selected item.
            is_double_click (bool): True if it's a double-click event, False otherwise.

        This method is called when an item is selected from the list, and it updates the selected item in the preview text.

        """
        index = self._items.index(new_val)
        self.selected_index = index
        self._list_panel.visible = False

        if self._on_selection_changed_handler is not None:
            self._on_selection_changed_handler(new_val, self.selected_index)

    def add_item(self, item: str):
        """
        Add an item to the list.

        Args:
            item (str): The item to be added to the list.

        """
        self._items.append(item)
        self._list.set_items(self._items)

    def clear_items(self):
        """Clear all items from the list."""
        self._items.clear()
        self._list.set_items(self._items)

    @property
    def selected_index(self) -> int:
        """
        Get the index of the currently selected item in the list.

        Returns:
            int: The index of the currently selected item.

        """
        return self._list.selected_index

    @selected_index.setter
    def selected_index(self, index: int):
        """
        Set the index of the currently selected item in the list.

        Args:
            index (int): The index of the item to be selected.

        """
        self._list.selected_index = index
        self._preview_text.text_value = self._items[index]

    def set_on_selection_changed(self, callback: Callable[[str, int], None]):
        """
        Set an event handler for when the selection changes in the list.

        Args:
            callback (Callable[[str, int], None]): The event handler function to be called when the selection changes.

        """
        self._on_selection_changed_handler = callback
