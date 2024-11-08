from typing import Union

import wx

from duit.event.Event import Event
from duit.ui.wx import WxUtils


class WxNumberField(wx.TextCtrl):
    def __init__(self, parent: wx.Window, id: int = wx.ID_ANY, value: Union[int, float] = 0,
                 min_value: Union[int, float] = WxUtils.MIN_INT32,
                 max_value: Union[int, float] = WxUtils.MAX_INT32,
                 precision: Union[int] = 3,
                 integer_only: bool = False,
                 *args, **kwargs):
        """
        Custom TextCtrl for handling numerical inputs.

        Args:
            parent (wx.Window): The parent window.
            id (int): Window identifier. A value of -1 indicates a default value.
            value (Union[int, float]): Initial value of the field.
            min_value (Union[int, float]): Minimum allowed value. If None, there's no minimum limit.
            max_value (Union[int, float]): Maximum allowed value. If None, there's no maximum limit.
            precision (Union[int]): Number of decimal places to round the value to. If None, no rounding is done.
            integer_only (bool): If True, restricts input and values to integers only.
            *args: Additional positional arguments to be passed to wx.TextCtrl.
            **kwargs: Additional keyword arguments to be passed to wx.TextCtrl.
        """
        style = kwargs.pop('style', 0) | wx.TE_PROCESS_ENTER  # Add TE_PROCESS_ENTER style
        super().__init__(parent, id, value=str(value), style=style, *args, **kwargs)

        self.Bind(wx.EVT_KILL_FOCUS, self._validate_text)
        self.Bind(wx.EVT_TEXT_ENTER, self._validate_text)

        self.min_value: Union[int, float] = min_value
        self.max_value: Union[int, float] = max_value
        self.precision: Union[int] = precision
        self.integer_only: bool = integer_only

        self._value: Union[int, float] = value
        self._validate: bool = True

        self.on_changed: Event[Union[int, float]] = Event()

    @property
    def number_value(self) -> Union[int, float]:
        """
        Getter for the numerical value of the field.

        Returns:
            Union[int, float]: The numerical value of the field.
        """
        value = self._value
        if self.integer_only:
            return int(value)
        return value

    @number_value.setter
    def number_value(self, value: Union[int, float]):
        """
        Setter for the numerical value of the field.

        Args:
            value (Union[int, float]): The new numerical value to set.
        """
        value = min(max(value, self.min_value), self.max_value)

        if self.integer_only:
            value = int(value)
        else:
            value = float(value)

        last_value = self._value
        self._value = value

        if last_value != self._value:
            self.on_changed(value)

        # update ui
        self._update_ui()

    def _update_ui(self):
        """
        Updates the UI display of the field.
        """
        visual_value = round(self._value, self.precision)

        if self.integer_only:
            visual_value = int(visual_value)

        self._validate = False
        self.SetValue(str(visual_value))
        self._validate = True

    def _validate_text(self, _) -> bool:
        """
        Validates the text input of the field.

        Args:
            _: Unused argument (event).

        Returns:
            bool: True if the text input is valid, False otherwise.
        """
        if not self._validate:
            return False

        text_value = self.GetValue().strip()

        if text_value == "":
            self.number_value = 0
            return True

        try:
            n = float(text_value)
        except ValueError as ex:
            # could not be parsed
            self._update_ui()
            return False

        self.number_value = n
        return True
