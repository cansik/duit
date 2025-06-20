from typing import Optional

from nicegui import ui
from nicegui.element import Element

from duit.model.DataField import DataField
from duit.ui.BaseProperty import BaseProperty, M
from duit.ui.annotations import UIAnnotation
from duit.ui.annotations.TitleAnnoation import TitleAnnotation
from duit.ui.nicegui.NiceGUIFieldProperty import NiceGUIFieldProperty


class TitleProperty(NiceGUIFieldProperty[TitleAnnotation, DataField[str]]):
    def __init__(self, annotation: UIAnnotation, model: Optional[M] = None, hide_label: bool = False):
        super().__init__(annotation, model, hide_label=True)

    def create_field(self) -> Element:
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
