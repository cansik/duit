from nicegui import ui
from nicegui.element import Element

from duit.model.DataField import DataField
from duit.ui.BaseProperty import BaseProperty
from duit.ui.annotations.BooleanAnnotation import BooleanAnnotation
from duit.ui.nicegui.NiceGUIFieldProperty import NiceGUIFieldProperty


class BooleanProperty(NiceGUIFieldProperty[BooleanAnnotation, DataField]):
    """
    A class to represent a property that can be toggled as a boolean value 
    using a NiceGUI switch element.
    """

    def create_field(self) -> Element:
        """
        Creates a GUI switch element for the boolean property.

        :returns: A NiceGUI switch element for toggling the boolean value.
        """
        ann = self.annotation

        element = ui.switch()

        if self.annotation.read_only:
            element.enabled = False
            element.props("readonly")

        if ann.tooltip is not None and ann.tooltip != "":
            element.tooltip(ann.tooltip)

        @BaseProperty.suppress_updates
        def on_ui_changed(*args, **kwargs):
            self.model.value = element.value

        @BaseProperty.suppress_updates
        def on_model_changed(value: bool):
            element.value = bool(value)

        element.on_value_change(on_ui_changed)

        self.model.on_changed += on_model_changed
        self.model.fire_latest()

        return element
