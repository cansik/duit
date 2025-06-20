from enum import Enum
from typing import Optional, Dict

from duit.ui.annotations.UIAnnotation import UIAnnotation


class DialogType(Enum):
    OpenFile = 0
    OpenDirectory = 1
    SaveFile = 2


class PathAnnotation(UIAnnotation):
    def __init__(self, name: str, placeholder_text: str = "",
                 tooltip: str = "", readonly: bool = False,
                 title: str = "Please choose a path",
                 dialog_type: DialogType = DialogType.OpenFile,
                 filters: Optional[Dict[str, str]] = None
                 ):
        """
        Initialize a PathAnnotation.

        :param name: The name of the path annotation.
        :param placeholder_text: The placeholder text to display in the input field.
        :param tooltip: The tooltip text for the annotation.
        :param readonly: Whether the annotation is read-only (default is False).
        :param title: The title of the file dialog.
        :param dialog_type: The type of file dialog (default is DialogType.OpenFile).
        :param filters: Optional file filters in the form of a dictionary (e.g. ".py": "Python") (default is an empty dictionary).
        """
        super().__init__(name, tooltip, readonly)
        self.placeholder_text = placeholder_text
        self.title = title
        self.dialog_type = dialog_type
        self.filters = filters

        if self.filters is None:
            self.filters = {}
