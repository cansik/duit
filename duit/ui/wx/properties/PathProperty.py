from pathlib import Path
from typing import Optional

import wx
from wx import BoxSizer

from duit.model.DataField import DataField
from duit.ui.annotations.PathAnnotation import PathAnnotation, DialogType
from duit.ui.wx.WxFieldProperty import WxFieldProperty


class PathProperty(WxFieldProperty[PathAnnotation, DataField]):
    """
    Property class for handling PathAnnotation.

    This property generates a text input field for entering or selecting file or directory paths.

    """

    def __init__(self, annotation: PathAnnotation, model: Optional[DataField[Path]] = None):
        """
        Initialize a PathProperty.

        :param annotation: The PathAnnotation associated with this property.
        :param model: The data model for this property (default is None).
        """
        super().__init__(annotation, model)

    def create_field(self, parent: wx.Window) -> BoxSizer:
        """
        Create the field widget for the PathProperty.

        This method generates a path input field.

        :param parent: Parent window for the field widget.
        :return: The path input field widget.
        """
        style = 0
        if self.annotation.read_only:
            style |= wx.TE_READONLY

        field = wx.TextCtrl(parent, value="", style=style)

        if self.model.value is not None:
            field.SetValue(str(self.model.value))

        def on_ui_changed(event):
            if field.GetValue() != self.model.value:
                self.model.value = Path(field.GetValue())

        def on_model_changed(value):
            wx.CallAfter(field.SetValue, str(value))

        field.Bind(wx.EVT_KILL_FOCUS, on_ui_changed)
        self.model.on_changed += on_model_changed

        self.model.fire_latest()

        def on_select_path(event):
            current_path: Path = self.model.value
            if not current_path.exists():
                current_path = Path(".")

            if self.annotation.dialog_type == DialogType.OpenDirectory:
                dialog = wx.DirDialog(parent, self.annotation.title, str(self.model.value),
                                      wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
            else:
                dialog_flags = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT if self.annotation.dialog_type == DialogType.SaveFile else wx.FD_OPEN

                wildcards = []
                for file_type, description in self.annotation.filters.items():
                    wildcards.append(f"{description} ({file_type})")
                    wildcards.append(file_type)

                dialog = wx.FileDialog(parent, self.annotation.title, str(current_path.parent), current_path.name,
                                       "|".join(wildcards), dialog_flags)

            dialog_result = dialog.ShowModal()

            if dialog_result == wx.ID_OK:
                path = dialog.GetPath()
                self.model.value = Path(path)

        button = wx.Button(parent, label="...", size=(50, -1))
        button.Bind(wx.EVT_BUTTON, on_select_path)

        container = wx.BoxSizer(orient=wx.HORIZONTAL)
        container.Add(field, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)
        container.Add(button, flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL, border=5)

        return container
