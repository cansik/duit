from typing import Union

from nicegui import ui
from nicegui.element import Element

from duit.model.DataField import DataField
from duit.ui.BaseProperty import BaseProperty
from duit.ui.annotations.SliderAnnotation import SliderAnnotation
from duit.ui.nicegui.NiceGUIFieldProperty import NiceGUIFieldProperty
from duit.ui.nicegui.components.InputNumberField import InputNumberField


class SliderProperty(NiceGUIFieldProperty[SliderAnnotation, DataField]):
    """
    A property that represents a slider UI component linked to a data field.

    :param SliderAnnotation: The annotation providing configuration for the slider.
    :param DataField: The underlying data field model that the slider interacts with.
    """
    
    def create_field(self) -> Element:
        """
        Creates the slider field component and its associated input number field.

        This method sets up event handlers for synchronizing the slider and the input number field,
        and defines properties such as min, max, step size, and visibility based on the annotation.

        :returns: The created slider UI element.
        """
        ann = self.annotation

        is_integer_only = isinstance(self.model.value, int)
        step_size = 1.0 if is_integer_only else max(0.001, (ann.limit_max - ann.limit_min) / 100.0)

        if ann.step_size is not None:
            step_size = ann.step_size

        with ui.row(wrap=False).classes("gap-2 items-center"):
            slider = ui.slider(min=ann.limit_min,
                               max=ann.limit_max,
                               value=self.model.value,
                               step=step_size
                               ).props(self._default_props).classes("my-auto grow")

            number_filed = InputNumberField(number_value=self.model.value,
                                            min_value=ann.limit_min,
                                            max_value=ann.limit_max,
                                            precision=ann.decimal_precision
                                            ).props(self._default_props).classes("w-24")

        number_filed.set_visibility(ann.show_number_field)

        if ann.tooltip is not None and ann.tooltip != "":
            slider.tooltip(ann.tooltip)
            number_filed.tooltip(ann.tooltip)

        if self.annotation.read_only:
            slider.props("readonly")
            number_filed.props("readonly")

        @BaseProperty.suppress_updates
        def on_ui_changed(*args, **kwargs):
            self.model.value = number_filed.number_value
            slider.value = number_filed.number_value

        @BaseProperty.suppress_updates
        def on_model_changed(value: Union[int, float]):
            number_filed.value = value
            slider.value = number_filed.number_value

        def on_slider_event(_):
            number_filed.number_value = slider.value

        slider.on_value_change(on_slider_event)
        number_filed.on_number_changed += on_ui_changed
        self.model.on_changed += on_model_changed
        self.model.fire_latest()

        return slider
