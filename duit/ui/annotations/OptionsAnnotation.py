from typing import Any, Iterable

from duit.ui.annotations import UIAnnotation


class OptionsAnnotation(UIAnnotation):
    def __init__(self, name: str, options: Iterable[Any], readonly: bool = False):
        super().__init__(name, readonly)
        self.options = options