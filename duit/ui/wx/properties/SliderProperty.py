from typing import Optional

import wx

from duit.model.DataField import DataField
from duit.ui.annotations.SliderAnnotation import SliderAnnotation
from duit.ui.wx.WxFieldProperty import WxFieldProperty
from duit.ui.wx.widgets.WxNumberSlider import WxNumberSlider


class SliderProperty(WxFieldProperty[SliderAnnotation, DataField]):

    def __init__(self, annotation: SliderAnnotation, model: Optional[DataField] = None):
        super().__init__(annotation, model)

    def create_field(self, parent: wx.Window) -> wx.Control:
        initial_value = self.model.value

        field = WxNumberSlider(parent,
                               value=initial_value,
                               min_value=self.annotation.limit_min,
                               max_value=self.annotation.limit_max,
                               precision=self.annotation.decimal_precision,
                               integer_only=isinstance(initial_value, int))

        field.Enable(not self.annotation.read_only or self.annotation.copy_content)
        field.SetToolTip(self.annotation.tooltip)

        def on_dm_changed(value):
            field.number_value = value

        def on_ui_changed(value):
            print(f"SliderValue: {value}")
            self.model.value = field.number_value

        self.model.on_changed.append(on_dm_changed)
        field.on_changed += on_ui_changed

        self.model.fire_latest()
        return field
