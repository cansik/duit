from typing import Optional, Sequence

from duit.ui.annotations import UIAnnotation


class VectorAnnotation(UIAnnotation):
    def __init__(self, name: str, decimal_precision: int = 3, tooltip: str = "",
                 readonly: bool = False, copy_content: bool = False,
                 max_width: int = 80, spacing: int = 8,
                 labels: Optional[Sequence[str]] = None, hide_labels: bool = False):
        super().__init__(name, tooltip, readonly)
        self.decimal_precision = decimal_precision
        self.copy_content = copy_content
        self.max_width = max_width
        self.spacing = spacing
        self.labels = labels
        self.hide_labels = hide_labels
