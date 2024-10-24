import wx

from duit.model.DataField import DataField
from duit.ui.annotations.BooleanAnnotation import BooleanAnnotation
from duit.ui.wx.WxFieldProperty import WxFieldProperty


class BooleanProperty(WxFieldProperty[BooleanAnnotation, DataField]):
    def create_field(self, parent) -> wx.Window:
        """
        Create and return the GUI field for the boolean property.

        Args:
            parent: The parent widget where the field will be created.

        Returns:
            wx.Window: The created GUI field.
        """
        field = wx.CheckBox(parent, label=self.annotation.name)

        # Set tooltip
        if self.annotation.tooltip:
            field.SetToolTip(self.annotation.tooltip)

        # Set initial value and enable/disable based on read_only property
        field.SetValue(self.model.value)
        field.Enable(not self.annotation.read_only)

        # Define event handlers
        def on_dm_changed(value):
            field.SetValue(value)

        def on_ui_changed(event):
            self.model.value = field.GetValue()

        # Bind events
        self.model.on_changed.append(on_dm_changed)
        field.Bind(wx.EVT_CHECKBOX, on_ui_changed)

        self.model.fire_latest()
        return field
