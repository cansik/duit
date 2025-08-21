from typing import Union

from nicegui.element import Element

from duit.model.DataField import DataField
from duit.ui.annotations import NumberAnnotation
from duit.ui.nicegui.NiceGUIFieldProperty import NiceGUIFieldProperty
from duit.ui.nicegui.NiceGUIPropertyBinder import NiceGUIPropertyBinder
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
            precision=ann.decimal_precision,
        ).props(self._default_props)

        if ann.read_only:
            element.props("readonly")

        if ann.tooltip:
            element.tooltip(ann.tooltip)

        def register_ui_change(cb):
            element.on_number_changed += cb

        self._binder = NiceGUIPropertyBinder[Union[int, float]](
            element=element,
            model=self.model,
            register_ui_change=register_ui_change,
            to_model=None,
            to_ui=None,
        )

        return element
