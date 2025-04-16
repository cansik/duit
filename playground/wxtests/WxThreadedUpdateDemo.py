import threading
import time

import wx


def main():
    app = wx.App(False)
    frame = wx.Frame(None, title="Demo", size=(640, 480))

    # Add an exit command to the File menu
    def exit_app(event):
        frame.Close(True)

    frame.Bind(wx.EVT_MENU, exit_app, id=wx.ID_EXIT)

    # Create a panel and text field
    panel = wx.Panel(frame)
    text_field = wx.TextCtrl(panel, value="Hello World")

    # Center the text field using a box sizer
    sizer = wx.BoxSizer(wx.VERTICAL)
    sizer.Add(text_field, 0, wx.ALL | wx.CENTER, 20)
    panel.SetSizer(sizer)

    def update_loop():
        counter = 0
        while True:
            time.sleep(0.3)

            wx.CallAfter(lambda: text_field.SetValue(f"{counter}"))
            counter += 1

    threading.Thread(target=update_loop, daemon=True).start()

    frame.Show(True)
    app.MainLoop()


if __name__ == "__main__":
    main()
