from typing import Optional, List, Union

from nicegui.elements.mixins.validation_element import ValidationFunction, ValidationDict
from nicegui.events import Handler, ValueChangeEventArguments

from duit.event.Event import Event
from duit.ui.nicegui.components.InputTextField import InputTextField


class InputNumberField(InputTextField):
    """
    A numeric input field that extends InputTextField to handle numerical values with validation.

    :param number_value: The initial numeric value.
    :param min_value: The minimum allowed numeric value.
    :param max_value: The maximum allowed numeric value.
    :param precision: The number of decimal places to retain for floating-point values.
    :param label: Optional label for the input field.
    :param placeholder: Optional placeholder text in the input field.
    :param value: Initial value of the input field as a string.
    :param password: Boolean flag to indicate if this field is a password field.
    :param password_toggle_button: Flag to indicate if a toggle button for password visibility should be displayed.
    :param on_change: Optional handler to be called when the value changes.
    :param autocomplete: List of autocomplete suggestions.
    :param validation: Optional validation function or dictionary.
    """
    
    def __init__(self,
                 number_value: Union[int, float],
                 min_value: Union[int, float],
                 max_value: Union[int, float],
                 precision: int = 3,
                 label: Optional[str] = None, *,
                 placeholder: Optional[str] = None,
                 value: str = '',
                 password: bool = False,
                 password_toggle_button: bool = False,
                 on_change: Optional[Handler[ValueChangeEventArguments]] = None,
                 autocomplete: Optional[List[str]] = None,
                 validation: Optional[Union[ValidationFunction, ValidationDict]] = None,
                 ) -> None:
        super().__init__(label, placeholder=placeholder, value=value, password=password,
                         password_toggle_button=password_toggle_button, on_change=on_change, autocomplete=autocomplete,
                         validation=validation)

        self.on_number_changed: Event[Union[int, float]] = Event()

        self.is_integer_only = isinstance(number_value, int)
        self.min_value = min_value
        self.max_value = max_value
        self.precision = precision

        self._number_value: Union[int, float] = 0

        self._is_silent = False
        self.on_input_changed += self._on_input_changed

        # update value
        self.number_value = number_value

    def _on_input_changed(self, text: str):
        """
        Handles input change events by attempting to convert input text to a numeric value.

        :param text: The text input by the user.
        """
        if self._is_silent:
            return

        # remember the last valid number
        prev = self.number_value
        try:
            # try to parse the new text
            num = float(text)
            self.number_value = self._convert_number(num)
        except (ValueError, TypeError):
            self.number_value = prev

    def _convert_number(self, value: Union[int, float]) -> Union[int, float]:
        """
        Ensures the number is within the specified bounds and returns it.

        :param value: The numeric value to convert.
        :returns: The bounded numeric value as an integer or float based on is_integer_only flag.
        """
        value = max(min(value, self.max_value), self.min_value)

        if self.is_integer_only:
            return int(value)
        return value

    def _format_number(self, value: Union[int, float]) -> str:
        """
        Format a number as a string based on integer-only mode and precision.

        :param value: The numeric value to format.
        :returns: The formatted number as a string.
        """
        if self.is_integer_only:
            return str(int(value))
        return f"{float(value):.{self.precision}f}"

    @property
    def number_value(self) -> Union[int, float]:
        """
        Gets the current numeric value of the input field.

        :returns: The current numeric value.
        """
        return self._number_value

    @number_value.setter
    def number_value(self, value: Union[int, float]):
        """
        Sets a new numeric value for the input field after validating and formatting it.

        :param value: The numeric value to set.
        """
        new_number = self._convert_number(value)

        # only update if it is a new number
        tolerance = 1e-9
        if abs(self._number_value - new_number) < tolerance:
            return

        self._number_value = new_number

        self._is_silent = True
        self.value = self._format_number(self._number_value)
        self.on_number_changed(self._number_value)
        self._is_silent = False
