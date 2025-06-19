from typing import List, Any

import wx

from duit.model.DataField import DataField
from duit.ui.annotations.OptionsAnnotation import OptionsAnnotation
from duit.ui.wx.WxFieldProperty import WxFieldProperty


class OptionsProperty(WxFieldProperty[OptionsAnnotation, DataField]):
    def create_field(self, parent) -> wx.Window:
        """
        Create an options field for the given boolean annotation.

        Args:
            parent: The parent widget.

        Returns:
            wx.Choice: The created options field.
        """
        str_options = [self.get_option_name(o) for o in self.options]
        field = wx.Choice(parent, choices=str_options)
        field.Enable(not self.annotation.read_only)

        if self.annotation.tooltip:
            field.SetToolTip(self.annotation.tooltip)

        def on_dm_changed(value):
            if value in self.options:
                index = self.options.index(value)
                self.silent_ui_update(field.SetSelection, index)

        def on_ui_changed(event):
            if self.is_ui_silent:
                return

            selection = event.GetSelection()
            self.model.value = self.options[selection]

        self.model.on_changed.append(on_dm_changed)
        field.Bind(wx.EVT_CHOICE, on_ui_changed)

        self.model.fire_latest()
        return field

    @property
    def options(self) -> List[Any]:
        """
        Get the list of options associated with the annotation.

        Returns:
            List[Any]: The list of options.
        """
        return self.annotation.options

    def get_option_name(self, option) -> str:
        """
        Get the name of an option as a string.

        Args:
            option: The option.

        Returns:
            str: The name of the option as a string.
        """
        return str(option)
