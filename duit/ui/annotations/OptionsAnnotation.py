from typing import Any, Iterable

from duit.ui.annotations import UIAnnotation


class OptionsAnnotation(UIAnnotation):
    def __init__(self, name: str, options: Iterable[Any], tooltip: str = "", readonly: bool = False):
        super().__init__(name, tooltip, readonly)
        self.options = options
