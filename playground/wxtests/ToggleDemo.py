import wx
import wx.adv

from duit.ui.wx.widgets.WxToggleSwitch import WxToggleSwitch


class ToggleFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Custom Toggle Example", size=(200, 100))
        panel = wx.Panel(self)

        self.toggle = WxToggleSwitch(panel, size=wx.Size(60, 30))

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.toggle, flag=wx.CENTER | wx.ALL, border=20)
        panel.SetSizer(sizer)


if __name__ == "__main__":
    app = wx.App(False)
    frame = ToggleFrame()
    frame.Show()
    app.MainLoop()
