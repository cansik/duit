from typing import Optional

import wx

from duit.annotation.Annotation import M
from duit.model.DataField import DataField
from duit.ui.annotations.TitleAnnoation import TitleAnnotation
from duit.ui.wx.WxFieldProperty import WxFieldProperty


class TitleProperty(WxFieldProperty[TitleAnnotation, DataField]):
    def __init__(self, annotation: TitleAnnotation, model: Optional[M] = None, hide_label: bool = False):
        super().__init__(annotation, model, hide_label=True)

    def create_field(self, parent: wx.Window) -> wx.Window:
        """
        Create a title widget for the given title annotation in wxPython.

        Args:
            parent: The parent wxPython widget.

        Returns:
            wx.TextCtrl: The created text entry widget.
        """
        style = 0
        if self.annotation.read_only:
            style |= wx.TE_READONLY

        field = wx.StaticText(parent, style=style)

        font: wx.Font = field.GetFont()
        font.SetPointSize(14)  # Set font size (e.g., 14 points)
        font.SetWeight(wx.FONTWEIGHT_BOLD)  # Set font weight to bold

        # Apply the modified font
        field.SetFont(font)

        if self.annotation.text_color is not None:
            field.SetForegroundColour(wx.Colour(*self.annotation.text_color))

        if self.model.value is not None:
            wx.CallAfter(field.SetLabelText, str(self.model.value))

        self.model.on_changed(lambda value: field.SetLabelText(str(value)))

        return field, wx.Panel(parent)
