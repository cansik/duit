import sys

from duit.ui.annotations.UIAnnotation import UIAnnotation


class NumberAnnotation(UIAnnotation):
    def __init__(self, name: str, limit_min: float = -sys.maxsize - 1, limit_max: float = sys.maxsize,
                 decimal_precision: int = 3,
                 tooltip: str = "", readonly: bool = False, copy_content: bool = False):
        """
        Initialize a NumberAnnotation.

        :param name: The name of the number annotation.
        :param limit_min: The minimum allowable value for the number (default is negative infinity).
        :param limit_max: The maximum allowable value for the number (default is positive infinity).
        :param decimal_precision: The number of decimal places to display for the number.
        :param tooltip: The tooltip text for the annotation.
        :param readonly: Whether the annotation is read-only (default is False).
        :param copy_content: Whether to enable content copying (default is False).
        """
        super().__init__(name, tooltip, readonly)
        self.limit_max = limit_max
        self.limit_min = limit_min
        self.copy_content = copy_content
        self.decimal_precision = decimal_precision
