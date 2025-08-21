from nicegui.element import Element

from duit.model.DataField import DataField
from duit.ui.annotations.TextAnnotation import TextAnnotation
from duit.ui.nicegui.NiceGUIFieldProperty import NiceGUIFieldProperty
from duit.ui.nicegui.NiceGUIPropertyBinder import NiceGUIPropertyBinder
from duit.ui.nicegui.components.InputTextField import InputTextField


class TextProperty(NiceGUIFieldProperty[TextAnnotation, DataField[str]]):
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

        if ann.tooltip:
            element.tooltip(ann.tooltip)

        if ann.read_only:
            element.props("readonly")

        def register_ui_change(cb):
            element.on_input_changed += cb

        self._binder = NiceGUIPropertyBinder[str](
            element=element,
            model=self.model,
            register_ui_change=register_ui_change,
            to_model=str,
            to_ui=str,
        )

        return element
