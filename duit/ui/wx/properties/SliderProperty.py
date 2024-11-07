from typing import Optional

import wx

from duit.model.DataField import DataField
from duit.ui.annotations.SliderAnnotation import SliderAnnotation
from duit.ui.wx.WxFieldProperty import WxFieldProperty
from duit.ui.wx.widgets.WxNumberField import WxNumberField
from duit.ui.wx.widgets.WxNumberSlider import WxNumberSlider


class SliderProperty(WxFieldProperty[SliderAnnotation, DataField]):

    def __init__(self, annotation: SliderAnnotation, model: Optional[DataField] = None):
        super().__init__(annotation, model)

    def create_field(self, parent: wx.Window) -> wx.Control:
        initial_value = self.model.value

        slider = WxNumberSlider(parent,
                                value=initial_value,
                                min_value=self.annotation.limit_min,
                                max_value=self.annotation.limit_max,
                                precision=self.annotation.decimal_precision,
                                integer_only=isinstance(initial_value, int))

        slider.Enable(not self.annotation.read_only or self.annotation.copy_content)
        slider.SetToolTip(self.annotation.tooltip)

        field = WxNumberField(parent,
                              value=initial_value,
                              min_value=self.annotation.limit_min,
                              max_value=self.annotation.limit_max,
                              precision=self.annotation.decimal_precision,
                              integer_only=isinstance(initial_value, int),
                              size=(65, -1))

        field.Enable(not self.annotation.read_only or self.annotation.copy_content)
        field.SetToolTip(self.annotation.tooltip)

        def on_dm_changed(value):
            def _update_ui():
                slider.number_value = value
                field.number_value = value

            self.silent_ui_update(_update_ui)

        def on_ui_changed(value):
            if self.is_ui_silent:
                return

            self.model.value = value

        self.model.on_changed.append(on_dm_changed)
        slider.on_changed += on_ui_changed
        field.on_changed += on_ui_changed

        self.model.fire_latest()

        hbox = wx.BoxSizer(orient=wx.HORIZONTAL)
        hbox.Add(slider, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)
        hbox.Add(field, flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL, border=5)

        return hbox
