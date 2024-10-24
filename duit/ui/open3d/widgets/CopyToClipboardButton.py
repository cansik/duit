import pyperclip
from open3d.cpu.pybind.visualization import gui

from duit.model.DataField import DataField


class CopyToClipboardButton(gui.Button):
    def __init__(self, field: DataField):
        """
        Initializes a CopyToClipboardButton instance.

        Args:
            field (DataField): The data field whose content will be copied to the clipboard.
        """
        super().__init__("»")
        self.tooltip = "Copy to Clipboard"
        self.horizontal_padding_em = 0
        self.vertical_padding_em = 0

        self.field = field

        self.set_on_clicked(self._copy_content)

    def _copy_content(self):
        """
        Copies the content of the associated data field to the system clipboard.
        """
        pyperclip.copy(self.field.value)
