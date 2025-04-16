import wx

from duit.model.DataField import DataField
from duit.ui.annotations.ProgressAnnotation import ProgressAnnotation
from duit.ui.wx.WxFieldProperty import WxFieldProperty


class ProgressProperty(WxFieldProperty[ProgressAnnotation, DataField]):
    GAUGE_RESOLUTION = 1024

    def create_field(self, parent) -> wx.Gauge:
        """
        Creates a progress bar for the DataField.

        Args:
            parent: The parent widget.

        Returns:
            wx.Gauge: The created progress bar.
        """
        field = wx.Gauge(parent, range=self.GAUGE_RESOLUTION, style=wx.GA_HORIZONTAL)
        field.Enable(not self.annotation.read_only)

        def on_dm_changed(value):
            progress_value = round(self.GAUGE_RESOLUTION * value)
            wx.CallAfter(field.SetValue, progress_value)

        self.model.on_changed.append(on_dm_changed)

        self.model.fire_latest()
        return field
