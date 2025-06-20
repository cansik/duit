from nicegui import ui
from nicegui.element import Element

from duit.model.DataField import DataField
from duit.ui.BaseProperty import BaseProperty
from duit.ui.annotations.ProgressAnnotation import ProgressAnnotation
from duit.ui.nicegui.NiceGUIFieldProperty import NiceGUIFieldProperty


class ProgressProperty(NiceGUIFieldProperty[ProgressAnnotation, DataField]):
    """
    A property class for managing a progress field in a NiceGUI application.

    This class integrates a ProgressAnnotation with a DataField, providing visual feedback 
    through a linear progress bar.

    :param annotation: The ProgressAnnotation that defines the properties of the progress field.
    :param model: The DataField model that holds the progress value and can trigger updates.
    """

    def create_field(self) -> Element:
        """
        Creates and configures a linear progress element based on the associated annotation.

        This method sets up the progress bar with its properties, including tooltip and read-only state,
        and binds it to the model to respond to changes.

        :returns: The configured linear progress UI element.
        """
        ann = self.annotation

        element = ui.linear_progress().props(self._default_props).classes('my-auto').props("animation-speed=300")

        if ann.tooltip is not None and ann.tooltip != "":
            element.tooltip(ann.tooltip)

        if self.annotation.read_only:
            element.props("readonly")

        @BaseProperty.suppress_updates
        def on_model_changed(value: float):
            """
            Updates the progress bar's value when the model changes.

            :param value: The new value to be set for the progress bar, as a float.
            """
            element.value = value

        self.model.on_changed += on_model_changed
        self.model.fire_latest()

        return element
