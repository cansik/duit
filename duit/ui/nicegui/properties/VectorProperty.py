import sys
from typing import Dict

from nicegui import ui
from nicegui.element import Element

from duit.model.DataField import DataField
from duit.ui.BaseProperty import BaseProperty
from duit.ui.annotations.VectorAnnotation import VectorAnnotation
from duit.ui.nicegui.NiceGUIFieldProperty import NiceGUIFieldProperty
from duit.ui.nicegui.components.InputNumberField import InputNumberField
from duit.utils import _vector


class VectorProperty(NiceGUIFieldProperty[VectorAnnotation, DataField]):
    """
    A class to create a UI component for editing vector properties in a NiceGUI application.

    :param annotation: A VectorAnnotation instance that defines the properties of the vector.
    :param model: A DataField instance that holds the vector data.
    """

    def create_field(self) -> Element:
        """
        Create a vector entry widget using NiceGUI NumberFields for each component of the vector.

        This method initializes the UI components and binds them to the underlying model. 
        Each component of the vector (e.g., x, y, z, t) is represented by a NumberField.

        :returns: A NiceGUI Element representing the row of number fields for the vector components.
        """
        ann = self.annotation
        attrs = _vector.get_vector_attributes(self.model.value)
        labels = list(ann.labels) if ann.labels is not None else attrs
        number_fields: Dict[str, InputNumberField] = {}

        row = ui.row(wrap=False).classes("gap-2 items-center")
        with row:
            for name, label_text in zip(attrs, labels):
                if not ann.hide_labels:
                    label = ui.label(f"{label_text}:")

                field = (
                    InputNumberField(
                        number_value=getattr(self.model.value, name),
                        min_value=-sys.maxsize - 1,
                        max_value=sys.maxsize,
                        precision=ann.decimal_precision
                    )
                    .props(self._default_props).classes("grow")
                )

                if ann.hide_labels:
                    field.tooltip(label_text)

                if ann.tooltip:
                    field.tooltip(ann.tooltip)

                if ann.read_only:
                    field.props("readonly")

                @BaseProperty.suppress_updates
                def on_ui_changed(value, name=name):
                    setattr(self.model.value, name, value)
                    self.model.fire()

                field.on_number_changed += on_ui_changed
                number_fields[name] = field

        @BaseProperty.suppress_updates
        def on_model_changed(value):
            for name in attrs:
                number_fields[name].number_value = getattr(self.model.value, name)

        self.model.on_changed += on_model_changed
        self.model.fire_latest()

        return row
