from nicegui import ui
from nicegui.element import Element

from duit.model.DataField import DataField
from duit.ui.annotations.BooleanAnnotation import BooleanAnnotation
from duit.ui.nicegui.NiceGUIFieldProperty import NiceGUIFieldProperty
from duit.ui.nicegui.NiceGUIPropertyBinder import NiceGUIPropertyBinder


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

        if ann.read_only:
            element.enabled = False
            element.props("readonly")

        if ann.tooltip:
            element.tooltip(ann.tooltip)

        def register_ui_change(cb):
            element.on_value_change(lambda ev: cb(bool(ev.value)))

        self._binder = NiceGUIPropertyBinder[bool](
            element=element,
            model=self.model,
            register_ui_change=register_ui_change,
            to_model=bool,
            to_ui=bool,
        )

        return element
