from typing import Any, Iterable

from duit.ui.annotations import UIAnnotation


class OptionsAnnotation(UIAnnotation):
    def __init__(self, name: str, options: Iterable[Any], tooltip: str = "", readonly: bool = False):
        """
        Initialize an OptionsAnnotation.

        :param name: The name of the options annotation.
        :param options: An iterable of available options for the annotation.
        :param tooltip: The tooltip text for the annotation.
        :param readonly: Whether the annotation is read-only (default is False).
        """
        super().__init__(name, tooltip, readonly)
        self.options = options
