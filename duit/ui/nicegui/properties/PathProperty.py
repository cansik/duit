from pathlib import Path
from typing import Optional

from nicegui import ui
from nicegui.element import Element

from duit.model.DataField import DataField
from duit.ui.BaseProperty import BaseProperty
from duit.ui.annotations.PathAnnotation import PathAnnotation
from duit.ui.nicegui.NiceGUIFieldProperty import NiceGUIFieldProperty


class PathProperty(NiceGUIFieldProperty[PathAnnotation, DataField[Optional[Path]]]):

    def create_field(self) -> Element:
        ann = self.annotation

        element = ui.input(placeholder=ann.placeholder_text).props(self._default_props)

        element.set_enabled(not ann.read_only)
        element.set_autocomplete([])

        if ann.tooltip is not None and ann.tooltip != "":
            element.tooltip(ann.tooltip)

        # todo: Also implement ann.copy_content

        @BaseProperty.suppress_updates
        def on_ui_changed(*args, **kwargs):
            self.model.value = element.value

        @BaseProperty.suppress_updates
        def on_model_changed(value: str):
            element.value = str(value)

        element.on("keydown.enter", on_ui_changed)
        element.on("blur", on_ui_changed)

        self.model.on_changed += on_model_changed
        self.model.fire_latest()

        return element
