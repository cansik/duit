from duit.ui.annotations.UIAnnotation import UIAnnotation


class ProgressAnnotation(UIAnnotation):
    def __init__(self, name: str, tooltip: str = ""):
        super().__init__(name, tooltip)