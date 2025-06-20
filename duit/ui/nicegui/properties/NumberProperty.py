from typing import Union

from nicegui.element import Element

from duit.model.DataField import DataField
from duit.ui.BaseProperty import BaseProperty
from duit.ui.annotations import NumberAnnotation
from duit.ui.nicegui.NiceGUIFieldProperty import NiceGUIFieldProperty
from duit.ui.nicegui.components.InputNumberField import InputNumberField


class NumberProperty(NiceGUIFieldProperty[NumberAnnotation, DataField]):
    def create_field(self) -> Element:
        ann = self.annotation

        element = InputNumberField(
            number_value=self.model.value,
            min_value=ann.limit_min,
            max_value=ann.limit_max,
            precision=ann.decimal_precision
        ).props(self._default_props)

        if self.annotation.read_only:
            element.props("readonly")

        if ann.tooltip is not None and ann.tooltip != "":
            element.tooltip(ann.tooltip)

        @BaseProperty.suppress_updates
        def on_ui_changed(value: Union[int, float]):
            self.model.value = value

        @BaseProperty.suppress_updates
        def on_model_changed(value: Union[int, float]):
            element.number_value = value

        element.on_number_changed += on_ui_changed
        self.model.on_changed += on_model_changed
        self.model.fire_latest()

        return element
