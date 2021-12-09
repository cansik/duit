from simbi.ui.annotations.UIAnnotation import UIAnnotation


class TextAnnotation(UIAnnotation):
    def __init__(self, name: str, placeholder_text: str = "", readonly: bool = False):
        super().__init__(name)
        self.placeholder_text = placeholder_text
        self.readonly = readonly
