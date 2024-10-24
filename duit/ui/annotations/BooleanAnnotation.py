from duit.ui.annotations.UIAnnotation import UIAnnotation


class BooleanAnnotation(UIAnnotation):
    def __init__(self, name: str, tooltip: str = "", readonly: bool = False):
        """
        Initialize a BooleanAnnotation.

        :param name: The name of the boolean annotation.
        :param tooltip: The tooltip text for the annotation.
        :param readonly: Whether the annotation is read-only (default is False).
        """
        super().__init__(name, tooltip, readonly)
