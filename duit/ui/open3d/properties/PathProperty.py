from pathlib import Path
from typing import Optional

from open3d.cpu.pybind.visualization.gui import Widget
from open3d.visualization import gui

from duit.model.DataField import DataField
from duit.ui.annotations.PathAnnotation import PathAnnotation, DialogType
from duit.ui.open3d import Open3dContext
from duit.ui.open3d.Open3dFieldProperty import Open3dFieldProperty


class PathProperty(Open3dFieldProperty[PathAnnotation, DataField]):
    """
    Property class for handling PathAnnotation.

    This property generates a text input field for entering or selecting file or directory paths.

    """

    def __init__(self, annotation: PathAnnotation, model: Optional[DataField] = None):
        """
        Initialize a PathProperty.

        :param annotation: The PathAnnotation associated with this property.
        :param model: The data model for this property (default is None).
        """
        super().__init__(annotation, model)

    def create_field(self) -> Widget:
        """
        Create the field widget for the PathProperty.

        This method generates a text input field for entering or selecting file or directory paths.

        :return: The text input field widget.
        """
        field = gui.TextEdit()
        field.placeholder_text = self.annotation.placeholder_text
        field.enabled = not self.annotation.read_only
        field.tooltip = self.annotation.tooltip

        def on_dm_changed(value: Path):
            field.text_value = str(value)

        def on_ui_changed(value):
            if self.annotation.read_only:
                field.text_value = str(self.model.value)
            else:
                self.model.value = Path(value)

        self.model.on_changed.append(on_dm_changed)
        field.set_on_value_changed(on_ui_changed)

        self.model.fire_latest()

        def on_select_path():
            if self.annotation.dialog_type == DialogType.OpenFile:
                dialog_type = gui.FileDialog.OPEN
            elif self.annotation.dialog_type == DialogType.OpenDirectory:
                dialog_type = gui.FileDialog.OPEN_DIR
            elif self.annotation.dialog_type == DialogType.SaveFile:
                dialog_type = gui.FileDialog.SAVE
            else:
                dialog_type = gui.FileDialog.OPEN

            window = Open3dContext.OPEN3D_MAIN_WINDOW
            dialog = gui.FileDialog(dialog_type, self.annotation.title, window.theme)
            dialog.set_path(str(self.model.value))

            if dialog_type == gui.FileDialog.OPEN or dialog_type == gui.FileDialog.SAVE:
                for file_type, description in self.annotation.filters.items():
                    dialog.add_filter(file_type, description)

            def on_cancel():
                window.close_dialog()

            def on_done(path: str):
                window.close_dialog()
                self.model.value = Path(path)

            dialog.set_on_done(on_done)
            dialog.set_on_cancel(on_cancel)
            window.show_dialog(dialog)

        select_path_btn = gui.Button("...")
        select_path_btn.tooltip = "Select path"
        select_path_btn.horizontal_padding_em = 0
        select_path_btn.vertical_padding_em = 0
        select_path_btn.set_on_clicked(on_select_path)

        container = gui.Horiz(4)
        container.add_child(field)
        container.add_child(select_path_btn)

        return container
