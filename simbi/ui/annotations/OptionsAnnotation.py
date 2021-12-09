from typing import Any, Iterable

from simbi.ui.annotations import UIAnnotation


class OptionsAnnotation(UIAnnotation):
    def __init__(self, name: str, options: Iterable[Any]):
        super().__init__(name)
        self.options = options