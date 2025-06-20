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
    """
    A class to handle a file or directory path property in a NiceGUI interface.
    This property allows for user interaction with file input through dialog boxes.
    """

    def create_field(self) -> Element:
        """
        Creates the UI field for the path property.

        :returns: An Element representing the input field for the path.
        """
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
            """
            Updates the model value when the UI input changes.

            :param args: Positional arguments.
            :param kwargs: Keyword arguments.
            """
            try:
                path = Path(element.value)
                self.model.value = path
            except:
                self.model.fire()

        @BaseProperty.suppress_updates
        def on_model_changed(value: str):
            """
            Updates the UI input element when the model value changes.

            :param value: The new value from the model.
            """
            element.value = str(value)

        select_button.on_click(self.pick_file)
        element.on_input_changed += on_ui_changed
        self.model.on_changed += on_model_changed
        self.model.fire_latest()

        return element

    async def pick_file(self) -> None:
        """
        Opens the appropriate file dialog based on the annotation configuration and
        updates the model with the selected path.
        """
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
        """
        Updates the model value with the selected path and notifies the user.

        :param paths: The list of paths selected by the user.
        """
        if paths is None:
            return

        path = paths[0]
        self.model.value = Path(paths[0])
        ui.notify(f"You chose {path}")
