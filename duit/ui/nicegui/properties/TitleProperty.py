from typing import Optional

from nicegui import ui
from nicegui.element import Element

from duit.model.DataField import DataField
from duit.ui.BaseProperty import BaseProperty, M
from duit.ui.annotations import UIAnnotation
from duit.ui.annotations.TitleAnnoation import TitleAnnotation
from duit.ui.nicegui.NiceGUIFieldProperty import NiceGUIFieldProperty


class TitleProperty(NiceGUIFieldProperty[TitleAnnotation, DataField[str]]):
    """
    A property to represent a title with specific UI annotation and model binding.

    :param annotation: The UI annotation that contains metadata for this title property.
    :param model: Optional model of type M to bind with the title property.
    :param hide_label: Boolean flag to indicate whether to hide the label.
    """
    
    def __init__(self, annotation: UIAnnotation, model: Optional[M] = None, hide_label: bool = False):
        super().__init__(annotation, model, hide_label=True)

    def create_field(self) -> Element:
        """
        Creates and configures the UI element for the title property.

        :returns: A NiceGUI Element representing the title with specific styles and properties.
        """
        ann = self.annotation
        element = ui.markdown(self.model.value).props(self._default_props).classes("col-span-full")

        if ann.text_color is not None:
            r, g, b = ann.text_color
            css_color = f"rgb({r}, {g}, {b})"
            element.style(f"color: {css_color};")

        if ann.tooltip is not None and ann.tooltip != "":
            element.tooltip(ann.tooltip)

        if self.annotation.read_only:
            element.props("readonly")

        @BaseProperty.suppress_updates
        def on_model_changed(value: str):
            element.value = value

        self.model.on_changed += on_model_changed
        self.model.fire_latest()

        return element
