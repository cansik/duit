import pyperclip
from open3d.cpu.pybind.visualization import gui

from duit.model.DataField import DataField


class CopyToClipboardButton(gui.Button):
    def __init__(self, field: DataField):
        super().__init__("»")
        self.tooltip = "Copy to Clipboard"
        self.horizontal_padding_em = 0
        self.vertical_padding_em = 0

        self.field = field

        self.set_on_clicked(self._copy_content)

    def _copy_content(self):
        pyperclip.copy(self.field.value)
