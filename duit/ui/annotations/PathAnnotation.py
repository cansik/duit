from enum import Enum
from pathlib import Path
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
        super().__init__(name, tooltip, readonly)
        self.placeholder_text = placeholder_text
        self.title = title
        self.dialog_type = dialog_type
        self.filters = filters

        if self.filters is None:
            self.filters = {}
