from typing import Union

import wx

from duit.event.Event import Event


class WxNumberSlider(wx.Slider):
    SLIDER_RESOLUTION = 1024

    def __init__(self, parent: wx.Window, id: int = wx.ID_ANY,
                 value: Union[int, float] = 0,
                 min_value: Union[int, float] = 0,
                 max_value: Union[int, float] = 100,
                 precision: Union[int] = 3,
                 integer_only: bool = False,
                 *args, **kwargs):

        style = kwargs.pop('style', 0) | wx.SL_HORIZONTAL
        super().__init__(parent, id, style=style, *args, **kwargs)

        self.Bind(wx.EVT_SLIDER, self._on_slider_event)

        self.SetRange(0, self.SLIDER_RESOLUTION)

        self.min_value: Union[int, float] = min_value
        self.max_value: Union[int, float] = max_value
        self.precision: Union[int] = precision
        self.integer_only: bool = integer_only

        self.on_changed: Event[Union[int, float]] = Event()

        self._value = value
        self.number_value = value

        self._update: bool = True

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

        self._update_ui()

    def _update_ui(self):
        self._update = False
        value = (self.number_value - self.min_value) / (self.max_value - self.min_value)
        slider_value = value * self.SLIDER_RESOLUTION
        self.SetValue(slider_value)
        self._update = True

    def _on_slider_event(self, event):
        if not self._update:
            return

        partial_value = self.GetValue() / self.SLIDER_RESOLUTION
        delta = (self.max_value - self.min_value) * partial_value
        actual_value = self.min_value + delta
        self.number_value = actual_value
