import sys

from duit.ui.annotations.UIAnnotation import UIAnnotation


class NumberAnnotation(UIAnnotation):
    def __init__(self, name: str, limit_min: float = -sys.maxsize - 1, limit_max: float = sys.maxsize,
                 decimal_precision: int = 3,
                 tooltip: str = "", readonly: bool = False, copy_content: bool = False):
        super().__init__(name, tooltip, readonly)
        self.limit_max = limit_max
        self.limit_min = limit_min
        self.copy_content = copy_content
        self.decimal_precision = decimal_precision
