import wx


class GreenPanel(wx.Window):
    def __init__(self, parent):
        super().__init__(parent)
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_MOTION, self.on_motion)

    def on_paint(self, event):
        dc = wx.PaintDC(self)
        dc.SetBrush(wx.Brush(wx.Colour(0, 255, 0)))  # Green background
        dc.DrawRectangle(0, 0, self.GetSize().GetWidth(), self.GetSize().GetHeight())

    def on_motion(self, event):
        print(f"Mouse position: {event.GetPosition()}")
        event.Skip()  # Ensure the event is processed further if needed


class MyApp(wx.App):
    def OnInit(self):
        frame = wx.Frame(None, title="Custom Component Example", size=(400, 300))
        panel = GreenPanel(frame)
        frame.Show(True)
        return True


if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()
