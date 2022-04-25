import sys

from duit.ui.annotations.UIAnnotation import UIAnnotation


class NumberAnnotation(UIAnnotation):
    def __init__(self, name: str, limit_min: float = -sys.maxsize - 1, limit_max: float = sys.maxsize,
                 readonly: bool = False):
        super().__init__(name, readonly)
        self.limit_max = limit_max
        self.limit_min = limit_min
