import sys
from typing import Union, Optional

from duit.ui.tk.widgets.CTkTextEntry import CTkTextEntry


class CTkNumberEntry(CTkTextEntry):
    def __init__(self, master: any,
                 initial_value: Union[int, float],
                 limit_min: float = -sys.maxsize - 1, limit_max: float = sys.maxsize,
                 decimal_precision: int = 3, **kwargs):
        super().__init__(master, **kwargs)

        self.initial_value = initial_value
        self.limit_min = limit_min
        self.limit_max = limit_max
        self.decimal_precision = decimal_precision

    @property
    def value(self) -> Optional[Union[int, float]]:
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
        if isinstance(number, int):
            self.text = f"{number}"
        else:
            self.text = f"{round(number, self.decimal_precision)}"

    @staticmethod
    def _is_number(value: str):
        try:
            float(value)
            return True
        except ValueError:
            return False
