from duit.ui.annotations import UIAnnotation


class ListAnnotation(UIAnnotation):
    def __init__(self, name: str, tooltip: str = "", readonly: bool = False):
        """
        Initialize a ListAnnotation.

        :param name: The name of the list annotation.
        :param tooltip: The tooltip text for the annotation.
        :param readonly: Whether the annotation is read-only (default is False).
        """
        super().__init__(name, tooltip, readonly)
