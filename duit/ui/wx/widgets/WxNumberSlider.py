from typing import Union

import wx

from duit.event.Event import Event


class WxNumberSlider(wx.Slider):
    SLIDER_RESOLUTION = 1024

    def __init__(self, parent: wx.Window, id: int = wx.ID_ANY,
                 value: Union[int, float] = 0,
                 min_value: Union[int, float] = 0,
                 max_value: Union[int, float] = 100,
                 precision: int = 3,
                 integer_only: bool = False,
                 *args, **kwargs):

        style = kwargs.pop('style', 0) | wx.SL_HORIZONTAL
        super().__init__(parent, id, style=style, *args, **kwargs)

        self.Bind(wx.EVT_SLIDER, self._on_slider_event)
        self.Bind(wx.EVT_LEFT_DOWN, self._on_left_click)

        self.SetRange(0, self.SLIDER_RESOLUTION)

        self._update = True
        self._suppress_events = False  # New flag to suppress unwanted events

        self.min_value = min_value
        self.max_value = max_value
        self.precision = precision
        self.integer_only = integer_only

        self.on_changed = Event()

        self._value = value
        self.number_value = value

    @property
    def number_value(self) -> Union[int, float]:
        value = self._value
        if self.integer_only:
            return int(value)
        return value

    @number_value.setter
    def number_value(self, value: Union[int, float]):
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
        if self._suppress_events:
            return
        self._update = False
        value = (self.number_value - self.min_value) / (self.max_value - self.min_value)
        slider_value = value * self.SLIDER_RESOLUTION
        self.SetValue(round(slider_value))
        self._update = True

    def _on_slider_event(self, event):
        if not self._update or self._suppress_events:
            return

        self._suppress_events = True  # Prevent triggering redundant updates
        try:
            partial_value = self.GetValue() / self.SLIDER_RESOLUTION
            delta = (self.max_value - self.min_value) * partial_value
            actual_value = self.min_value + delta
            self.number_value = actual_value
        finally:
            self._suppress_events = False

    def _on_left_click(self, event):
        if not self._update:
            return

        click_x = event.GetX()
        slider_width = self.GetSize().GetWidth() - 2 * self.GetThumbLength()
        fraction_clicked = max(0, min(1, click_x / slider_width))
        new_value = self.min_value + fraction_clicked * (self.max_value - self.min_value)

        self._suppress_events = True  # Prevent triggering slider events during update
        try:
            self.number_value = new_value
        finally:
            self._suppress_events = False

        event.Skip()  # Ensure the default event handling behavior is maintained
