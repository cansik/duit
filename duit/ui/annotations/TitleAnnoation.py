from typing import Tuple, Optional

from duit.ui.annotations.UIAnnotation import UIAnnotation


class TitleAnnotation(UIAnnotation):
    def __init__(self, text_color: Optional[Tuple[int, int, int]] = None, tooltip: str = ""):
        """
        Initialize a TitleAnnotation.

        :param text_color: The color of the text (RGB 0-255).
        :param tooltip: The tooltip text for the annotation.
        """
        super().__init__("", tooltip, True)
        self.text_color = text_color
