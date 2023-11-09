import sys
from typing import Union, Optional

from duit.ui.tk.widgets.CTkTextEntry import CTkTextEntry


class CTkNumberEntry(CTkTextEntry):
    def __init__(self, master: any,
                 initial_value: Union[int, float],
                 limit_min: float = -sys.maxsize - 1, limit_max: float = sys.maxsize,
                 decimal_precision: int = 3, **kwargs):
        """
        Initialize a CTkNumberEntry instance, which is a custom text entry field for numbers.

        Args:
            master (any): The parent widget.
            initial_value (Union[int, float]): The initial numeric value.
            limit_min (float, optional): The minimum limit for the numeric value. Defaults to -sys.maxsize - 1.
            limit_max (float, optional): The maximum limit for the numeric value. Defaults to sys.maxsize.
            decimal_precision (int, optional): The decimal precision for float values. Defaults to 3.
            **kwargs: Additional keyword arguments for the CTkTextEntry constructor.
        """
        super().__init__(master, **kwargs)

        self.initial_value = initial_value
        self.limit_min = limit_min
        self.limit_max = limit_max
        self.decimal_precision = decimal_precision

    @property
    def value(self) -> Optional[Union[int, float]]:
        """
        Get the numeric value from the text entry.

        Returns:
            Optional[Union[int, float]]: The numeric value, or None if the input is not a valid number.
        """
        content = self.text
        if not self._is_number(content):
            return

        value = float(content)
        value = max(self.limit_min, value)
        value = min(self.limit_max, value)

        if isinstance(self.initial_value, int):
            value = int(value)
        else:
            value = float(value)

        return value

    @value.setter
    def value(self, number: Union[int, float]):
        """
        Set the numeric value in the text entry.

        Args:
            number (Union[int, float]): The numeric value to set.
        """
        if isinstance(number, int):
            self.text = f"{number}"
        else:
            self.text = f"{round(number, self.decimal_precision)}"

    @staticmethod
    def _is_number(value: str):
        """
        Check if the provided value is a valid number.

        Args:
            value (str): The value to check.

        Returns:
            bool: True if the value is a valid number, otherwise False.
        """
        try:
            float(value)
            return True
        except ValueError:
            return False
