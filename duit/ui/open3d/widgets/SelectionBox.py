from typing import List, Callable, Optional

from open3d.cpu.pybind.visualization import gui


class SelectionBox(gui.Vert):
    def __init__(self):
        super().__init__()

        self.list_size: int = 200

        self._preview_text = gui.TextEdit()
        self._preview_text.enabled = False

        self._open_button = gui.Button("¬")
        self._open_button.vertical_padding_em = 0
        self._open_button.horizontal_padding_em = 0
        self._open_button.set_on_clicked(self._on_button_clicked)

        self._list = gui.ListView()
        self._list.background_color.set_color(1.0, 0.0, 0.0)
        self._list.set_on_selection_changed(self._on_list_selection_changed)
        self._list.visible = False

        container = gui.Horiz(4)
        container.add_child(self._preview_text)
        container.add_child(self._open_button)

        self.add_child(container)
        self.add_child(self._list)

        self._on_selection_changed_handler: Optional[Callable[[str, int], None]] = None

        self._items: List[str] = []

        self.background_color = gui.Color(255, 0, 0, 1)

    def _on_button_clicked(self):
        rect: gui.Rect = self.frame

        self._list.frame = gui.Rect(rect.x, rect.y + rect.height, rect.width, self.list_size)
        self._list.visible = True

    def _on_list_selection_changed(self, new_val, is_double_click):
        index = self._items.index(new_val)
        self.selected_index = index
        self._list.visible = False

        if self._on_selection_changed_handler is not None:
            self._on_selection_changed_handler(new_val, self.selected_index)

    def add_item(self, item: str):
        self._items.append(item)
        self._list.set_items(self._items)

    @property
    def selected_index(self) -> int:
        return self._list.selected_index

    @selected_index.setter
    def selected_index(self, value: int):
        self._list.selected_index = value
        self._preview_text.text_value = self._items[value]

    def set_on_selection_changed(self, callback: Callable[[str, int], None]):
        self._on_selection_changed_handler = callback
