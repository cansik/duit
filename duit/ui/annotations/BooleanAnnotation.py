from duit.ui.annotations.UIAnnotation import UIAnnotation


class BooleanAnnotation(UIAnnotation):
    def __init__(self, name: str, readonly: bool = False):
        super().__init__(name, readonly)
