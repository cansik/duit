from duit.ui.annotations import UIAnnotation


class VectorAnnotation(UIAnnotation):
    def __init__(self, name: str, decimal_precision: int = 3, tooltip: str = "",
                 readonly: bool = False, copy_content: bool = False):
        super().__init__(name, tooltip, readonly)
        self.decimal_precision = decimal_precision
        self.copy_content = copy_content
