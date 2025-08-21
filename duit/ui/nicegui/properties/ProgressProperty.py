from nicegui import ui
from nicegui.element import Element

from duit.model.DataField import DataField
from duit.ui.annotations.ProgressAnnotation import ProgressAnnotation
from duit.ui.nicegui.NiceGUIFieldProperty import NiceGUIFieldProperty
from duit.ui.nicegui.NiceGUIPropertyBinder import NiceGUIPropertyBinder


class ProgressProperty(NiceGUIFieldProperty[ProgressAnnotation, DataField[float]]):
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

        element = (
            ui.linear_progress()
            .props(self._default_props)
            .classes("my-auto")
            .props("animation-speed=300")
        )

        if ann.tooltip:
            element.tooltip(ann.tooltip)

        if ann.read_only:
            element.props("readonly")

        # Progress bar is one-way (model -> UI)
        def register_ui_change(cb):
            # no UI -> model events for progress bar
            pass

        self._binder = NiceGUIPropertyBinder[float](
            element=element,
            model=self.model,
            register_ui_change=register_ui_change,
            to_model=float,
            to_ui=float,
        )

        return element
