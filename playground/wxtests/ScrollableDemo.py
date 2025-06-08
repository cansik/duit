import wx
from abc import ABC, ABCMeta

# stub for your existing BasePropertyPanel
class BasePropertyPanel(ABC):
    pass

# combine the two metaclasses
class PanelMeta(type(wx.ScrolledWindow), ABCMeta):
    pass

class PanelMixin(wx.ScrolledWindow, BasePropertyPanel, ABC, metaclass=PanelMeta):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, style=wx.VSCROLL | wx.HSCROLL, *args, **kwargs)
        BasePropertyPanel.__init__(self)
        self.SetScrollRate(5, 5)
        self.SetAutoLayout(True)

class DemoPanel(PanelMixin):
    def __init__(self, parent):
        super().__init__(parent)

    def create_panel(self):
        # if you have logic around data_context, remove or adjust it
        # for this demo we just build 40 text boxes
        sizer = wx.BoxSizer(wx.VERTICAL)
        for i in range(40):
            txt = wx.TextCtrl(self, value=f"Text Box {i + 1}")
            sizer.Add(txt, 0, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(sizer)
        # now actually lay out and set the scrollable area
        self.Layout()
        self.FitInside()

class DemoFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Scrollable Demo", size=(300, 400))
        self.panel = DemoPanel(self)
        self.Show()

if __name__ == "__main__":
    app = wx.App(False)
    frame = DemoFrame()
    wx.CallLater(2000, lambda: frame.panel.create_panel())
    app.MainLoop()
