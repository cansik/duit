from duit.ui.annotations.UIAnnotation import UIAnnotation


class BooleanAnnotation(UIAnnotation):
    def __init__(self, name: str, tooltip: str = "", readonly: bool = False):
        super().__init__(name, tooltip, readonly)
