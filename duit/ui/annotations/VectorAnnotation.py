from typing import Optional, Sequence

from duit.ui.annotations import UIAnnotation


class VectorAnnotation(UIAnnotation):
    def __init__(self, name: str, decimal_precision: int = 3, tooltip: str = "",
                 readonly: bool = False, copy_content: bool = False,
                 max_width: float = 3.0, spacing: float = 0.25,
                 labels: Optional[Sequence[str]] = None, hide_labels: bool = False):
        """
        Initialize a VectorAnnotation.

        :param name: The name of the vector annotation.
        :param decimal_precision: The number of decimal places to display for each vector component.
        :param tooltip: The tooltip text for the annotation.
        :param readonly: Whether the annotation is read-only (default is False).
        :param copy_content: Whether to enable content copying (default is False).
        :param max_width: The maximum width for the vector display.
        :param spacing: The spacing between vector components.
        :param labels: Optional labels for the vector components (default is None).
        :param hide_labels: Whether to hide labels for the vector components (default is False).
        """
        super().__init__(name, tooltip, readonly)
        self.decimal_precision = decimal_precision
        self.copy_content = copy_content
        self.max_width = max_width
        self.spacing = spacing
        self.labels = labels
        self.hide_labels = hide_labels
