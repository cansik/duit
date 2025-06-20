from nicegui.element import Element

from duit.model.DataField import DataField
from duit.ui.BaseProperty import BaseProperty
from duit.ui.annotations.TextAnnotation import TextAnnotation
from duit.ui.nicegui.NiceGUIFieldProperty import NiceGUIFieldProperty
from duit.ui.nicegui.components.InputTextField import InputTextField


class TextProperty(NiceGUIFieldProperty[TextAnnotation, DataField]):
    """
    A property that manages a text input field for a given DataField, using a TextAnnotation for configuration.
    """

    def create_field(self) -> Element:
        """
        Creates a text input field based on the associated TextAnnotation.

        This method configures the input field with placeholder text, tooltip, and read-only state as specified in
        the annotation. It also sets up event listeners to synchronize changes between the UI and the underlying model.

        :returns: An Element representing the configured text input field.
        """
        ann = self.annotation

        element = InputTextField(placeholder=ann.placeholder_text).props(self._default_props)

        if ann.tooltip is not None and ann.tooltip != "":
            element.tooltip(ann.tooltip)

        if self.annotation.read_only:
            element.props("readonly")

        @BaseProperty.suppress_updates
        def on_ui_changed(*args, **kwargs):
            self.model.value = element.value

        @BaseProperty.suppress_updates
        def on_model_changed(value: str):
            element.value = str(value)

        element.on_input_changed += on_ui_changed
        self.model.on_changed += on_model_changed
        self.model.fire_latest()

        return element
