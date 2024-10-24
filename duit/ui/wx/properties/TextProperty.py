import wx
from duit.model.DataField import DataField
from duit.ui.annotations.TextAnnotation import TextAnnotation
from duit.ui.wx.WxFieldProperty import WxFieldProperty


class TextProperty(WxFieldProperty[TextAnnotation, DataField]):
    def create_field(self, parent: wx.Window) -> wx.Window:
        """
        Create a text entry widget for the given text annotation in wxPython.

        Args:
            parent: The parent wxPython widget.

        Returns:
            wx.TextCtrl: The created text entry widget.
        """
        style = 0
        if self.annotation.read_only:
            style |= wx.TE_READONLY

        field = wx.TextCtrl(parent, value="", style=style)

        if self.model.value is not None:
            field.SetValue(str(self.model.value))

        def on_ui_changed(event):
            if field.GetValue() != self.model.value:
                self.model.value = field.GetValue()

        field.Bind(wx.EVT_KILL_FOCUS, on_ui_changed)
        self.model.on_changed(lambda value: field.SetValue(str(value)))

        return field
