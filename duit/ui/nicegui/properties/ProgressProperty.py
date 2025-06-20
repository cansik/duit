from nicegui import ui
from nicegui.element import Element

from duit.model.DataField import DataField
from duit.ui.BaseProperty import BaseProperty
from duit.ui.annotations.ProgressAnnotation import ProgressAnnotation
from duit.ui.nicegui.NiceGUIFieldProperty import NiceGUIFieldProperty


class ProgressProperty(NiceGUIFieldProperty[ProgressAnnotation, DataField]):
    def create_field(self) -> Element:
        ann = self.annotation

        element = ui.linear_progress().props(self._default_props)

        if ann.tooltip is not None and ann.tooltip != "":
            element.tooltip(ann.tooltip)

        if self.annotation.read_only:
            element.props("readonly")

        @BaseProperty.suppress_updates
        def on_model_changed(value: float):
            element.value = value

        self.model.on_changed += on_model_changed
        self.model.fire_latest()

        return element
