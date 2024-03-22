import wx

from Config import Config
from duit.ui.wx.WxPropertyPanel import WxPropertyPanel
from duit.ui.wx.WxPropertyRegistry import init_wx_registry


def main():
    init_wx_registry()

    config = Config()

    app = wx.App(False)
    frame = wx.Frame(None, title="Configuration", size=(400, 600))

    # Create a menu bar
    menubar = wx.MenuBar()

    # Create a File menu
    file_menu = wx.Menu()
    menubar.Append(file_menu, "&File")

    # Add an exit command to the File menu
    def exit_app(event):
        frame.Close(True)

    file_menu.Append(wx.ID_EXIT, "E&xit", "Exit application")
    frame.Bind(wx.EVT_MENU, exit_app, id=wx.ID_EXIT)

    frame.SetMenuBar(menubar)

    panel = WxPropertyPanel(frame)
    sizer = wx.BoxSizer(wx.VERTICAL)
    frame.SetSizer(sizer)

    panel.data_context = config
    sizer.Add(panel, 1, wx.EXPAND)

    def on_hungry(value):
        print(f"Hungry changed to: {value}")

    def on_resolution_changed(value):
        print(f"Resolution: {value}")

    config.hungry.on_changed.append(on_hungry)
    config.resolution.on_changed.append(on_resolution_changed)

    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    main()
