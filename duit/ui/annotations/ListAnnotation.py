from duit.ui.annotations import UIAnnotation


class ListAnnotation(UIAnnotation):
    def __init__(self, name: str, tooltip: str = "", readonly: bool = False):
        super().__init__(name, tooltip, readonly)
