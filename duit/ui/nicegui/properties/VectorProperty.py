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
    def create_field(self) -> Element:
        """
        Create a vector entry widget using NiceGUI NumberFields for each component of the vector.
        """
        ann = self.annotation
        # get the attribute names (e.g. ['x', 'y', 'z'])
        attrs = _vector.get_vector_attributes(self.model.value)
        # determine labels for each component
        labels = list(ann.labels) if ann.labels is not None else attrs
        number_fields: Dict[str, InputNumberField] = {}

        # create a horizontal row to hold labels and fields
        row = ui.row(wrap=False).classes("gap-2 items-center")
        with row:
            for name, label_text in zip(attrs, labels):
                # handle hiding or showing per-component label
                if not ann.hide_labels:
                    label = ui.label(f"{label_text}:")

                # instantiate the number field with current value and precision
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
                    # use the component tooltip to show the label
                    field.tooltip(label_text)

                # attach tooltip if provided
                if ann.tooltip:
                    field.tooltip(ann.tooltip)

                # make read-only if annotation requires
                if ann.read_only:
                    field.props("readonly")

                # update model when user edits the field
                @BaseProperty.suppress_updates
                def on_ui_changed(value, name=name):
                    setattr(self.model.value, name, value)
                    self.model.fire()

                field.on_number_changed += on_ui_changed
                number_fields[name] = field

        # update UI fields if the model changes externally
        @BaseProperty.suppress_updates
        def on_model_changed(value):
            for name in attrs:
                number_fields[name].number_value = getattr(self.model.value, name)

        self.model.on_changed += on_model_changed
        # initialize UI to current model state
        self.model.fire_latest()

        return row
