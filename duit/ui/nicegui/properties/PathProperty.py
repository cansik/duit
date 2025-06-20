from pathlib import Path
from typing import Optional, List

from nicegui import ui
from nicegui.element import Element

from duit.model.DataField import DataField
from duit.ui.BaseProperty import BaseProperty
from duit.ui.annotations.PathAnnotation import PathAnnotation, DialogType
from duit.ui.nicegui.NiceGUIFieldProperty import NiceGUIFieldProperty
from duit.ui.nicegui.components.InputTextField import InputTextField
from duit.ui.nicegui.components.local_file_dialogs import OpenFilePicker, SaveFilePicker, OpenFolderPicker


class PathProperty(NiceGUIFieldProperty[PathAnnotation, DataField[Optional[Path]]]):
    def create_field(self) -> Element:
        ann = self.annotation

        with ui.row(wrap=False).classes("gap-1 items-center"):
            element = InputTextField(placeholder=ann.placeholder_text).props(self._default_props).classes("grow")
            select_button = ui.button(icon="s_folder_open").props(self._default_props)

        element.set_autocomplete([])

        if ann.tooltip is not None and ann.tooltip != "":
            element.tooltip(ann.tooltip)
            select_button.tooltip(ann.tooltip)

        if self.annotation.read_only:
            element.props("readonly")
            select_button.props("readonly")

        @BaseProperty.suppress_updates
        def on_ui_changed(*args, **kwargs):
            try:
                path = Path(element.value)
                self.model.value = path
            except:
                self.model.fire()

        @BaseProperty.suppress_updates
        def on_model_changed(value: str):
            element.value = str(value)

        select_button.on_click(self.pick_file)
        element.on_input_changed += on_ui_changed
        self.model.on_changed += on_model_changed
        self.model.fire_latest()

        return element

    async def pick_file(self) -> None:
        default_path = "~"
        default_file_name = ""

        if self.model.value is not None:
            path = self.model.value

            default_path = path.parent
            default_file_name = path.name

        if self.annotation.dialog_type == DialogType.OpenFile:
            result = await OpenFilePicker(default_path, title=self.annotation.title, multiple=False,
                                          show_hidden=True, filters=self.annotation.filters)
            self.update_path(result)
        elif self.annotation.dialog_type == DialogType.SaveFile:
            result = await SaveFilePicker(default_path, title=self.annotation.title,
                                          show_hidden=True, filters=self.annotation.filters,
                                          default_name=default_file_name)
            self.update_path(result)
        elif self.annotation.dialog_type == DialogType.OpenDirectory:
            result = await OpenFolderPicker(default_path, title=self.annotation.title, show_hidden=True)
            self.update_path(result)
        else:
            raise Exception(f"Dialog Type ({self.annotation.dialog_type}) is not allowed.")

    def update_path(self, paths: Optional[List[Path]]):
        if paths is None:
            return

        path = paths[0]
        self.model.value = Path(paths[0])
        ui.notify(f"You chose {path}")
