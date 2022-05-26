from duit.ui.annotations.UIAnnotation import UIAnnotation


class TextAnnotation(UIAnnotation):
    def __init__(self, name: str, placeholder_text: str = "",
                 readonly: bool = False, copy_content: bool = False):
        super().__init__(name, readonly)
        self.placeholder_text = placeholder_text
        self.copy_content = copy_content
