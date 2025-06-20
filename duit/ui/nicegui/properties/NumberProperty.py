from typing import Union

from nicegui.element import Element

from duit.model.DataField import DataField
from duit.ui.BaseProperty import BaseProperty
from duit.ui.annotations import NumberAnnotation
from duit.ui.nicegui.NiceGUIFieldProperty import NiceGUIFieldProperty
from duit.ui.nicegui.components.InputNumberField import InputNumberField


class NumberProperty(NiceGUIFieldProperty[NumberAnnotation, DataField]):
    """
    A property that represents a numeric input field with defined constraints.

    :param NumberAnnotation annotation: The annotation that provides metadata for the field.
    :param DataField model: The underlying data model associated with this property.
    """
    
    def create_field(self) -> Element:
        """
        Creates a numeric input field component with specified properties.

        The field is initialized with the current value from the model, 
        and it respects the limits and precision defined in the annotation. 
        Event handlers are set up to synchronize changes between the field 
        and the model.

        :returns: An Element representing the numeric input field.
        """
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
            """
            Updates the model value when the UI component's value changes.

            :param value: The new value from the UI, either an integer or a float.
            """
            self.model.value = value

        @BaseProperty.suppress_updates
        def on_model_changed(value: Union[int, float]):
            """
            Updates the UI component's value when the model's value changes.

            :param value: The new value from the model, either an integer or a float.
            """
            element.number_value = value

        element.on_number_changed += on_ui_changed
        self.model.on_changed += on_model_changed
        self.model.fire_latest()

        return element
