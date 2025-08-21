from typing import Union

from nicegui import ui
from nicegui.element import Element

from duit.model.DataField import DataField
from duit.ui.annotations.SliderAnnotation import SliderAnnotation
from duit.ui.nicegui.NiceGUIFieldProperty import NiceGUIFieldProperty
from duit.ui.nicegui.NiceGUIPropertyBinder import NiceGUIPropertyBinder
from duit.ui.nicegui.components.InputNumberField import InputNumberField


class SliderProperty(NiceGUIFieldProperty[SliderAnnotation, DataField[Union[int, float]]]):
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
            slider = (
                ui.slider(
                    min=ann.limit_min,
                    max=ann.limit_max,
                    value=self.model.value,
                    step=step_size,
                )
                .props(self._default_props)
                .classes("my-auto grow")
            )

            number_field = (
                InputNumberField(
                    number_value=self.model.value,
                    min_value=ann.limit_min,
                    max_value=ann.limit_max,
                    precision=ann.decimal_precision,
                )
                .props(self._default_props)
                .classes("w-24")
            )

        number_field.set_visibility(ann.show_number_field)

        if ann.tooltip:
            slider.tooltip(ann.tooltip)
            number_field.tooltip(ann.tooltip)

        if ann.read_only:
            slider.props("readonly")
            number_field.props("readonly")

        # binder from number_field -> model -> number_field
        def register_ui_change(cb):
            number_field.on_number_changed += cb

        def to_model(v: Union[int, float]) -> Union[int, float]:
            return v

        def to_ui(v: Union[int, float]) -> Union[int, float]:
            return v

        self._binder = NiceGUIPropertyBinder[Union[int, float]](
            element=number_field,
            model=self.model,
            register_ui_change=register_ui_change,
            to_model=to_model,
            to_ui=to_ui,
        )

        # keep slider and number_field in sync locally
        def on_slider_event(ev):
            number_field.number_value = ev.value

        slider.on_value_change(on_slider_event)

        def on_number_event(v):
            slider.value = number_field.number_value

        number_field.on_number_changed += on_number_event

        return slider
