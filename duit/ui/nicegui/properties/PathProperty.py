from pathlib import Path
from typing import Optional

from nicegui import ui
from nicegui.element import Element

from duit.model.DataField import DataField
from duit.ui.BaseProperty import BaseProperty
from duit.ui.annotations.PathAnnotation import PathAnnotation
from duit.ui.nicegui.NiceGUIFieldProperty import NiceGUIFieldProperty
from duit.ui.nicegui.components.InputTextField import InputTextField
from duit.ui.nicegui.components.LocalFilePicker import LocalFilePicker


class PathProperty(NiceGUIFieldProperty[PathAnnotation, DataField[Optional[Path]]]):
    def create_field(self) -> Element:
        ann = self.annotation

        with ui.row(wrap=False).classes("gap-1 items-center"):
            element = InputTextField(placeholder=ann.placeholder_text).props(self._default_props).classes("grow")
            select_button = ui.button(icon="s_folder_open").props(self._default_props)

        element.set_autocomplete([])

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

        select_button.on_click(self.pick_file)
        element.on_input_changed += on_ui_changed
        self.model.on_changed += on_model_changed
        self.model.fire_latest()

        return element

    async def pick_file(self) -> None:
        result = await LocalFilePicker('~', multiple=False)
        ui.notify(f'You chose {result}')
