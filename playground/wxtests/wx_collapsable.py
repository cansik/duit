import wx
import random
import string

def random_label():
    """Generate a random string to use as a label."""
    return ''.join(random.choices(string.ascii_letters, k=8))

class CollapsiblePaneApp(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Collapsible Pane Example", size=(400, 500))

        # Main panel
        panel = wx.Panel(self)

        # Create a collapsible pane
        collapsible_pane = wx.CollapsiblePane(panel, label="Click to Expand/Collapse")
        collapsible_pane.Collapse(False)

        # Bind the event to refresh layout on collapse/expand
        collapsible_pane.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self.on_pane_changed)

        # Populate the collapsible pane
        pane = collapsible_pane.GetPane()
        sizer = wx.FlexGridSizer(rows=10, cols=2, vgap=5, hgap=2)
        sizer.SetFlexibleDirection(wx.HORIZONTAL)
        sizer.AddGrowableCol(1, 1)

        for _ in range(10):
            label = wx.StaticText(pane, label=random_label())
            # Randomly choose a component to add
            component_type = random.choice(['textbox', 'checkbox', 'button', 'combobox'])
            if component_type == 'textbox':
                component = wx.TextCtrl(pane)
            elif component_type == 'checkbox':
                component = wx.CheckBox(pane, label="Option")
            elif component_type == 'button':
                component = wx.Button(pane, label="Click Me")
            elif component_type == 'combobox':
                component = wx.ComboBox(pane, choices=["Choice 1", "Choice 2", "Choice 3"], style=wx.CB_READONLY)

            sizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL, 5)
            sizer.Add(component, 1, wx.EXPAND, 5)

        pane.SetSizer(sizer)

        # Main sizer for the frame
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(collapsible_pane, 1, wx.ALL | wx.EXPAND, 10)
        panel.SetSizer(main_sizer)

        self.Layout()

    def on_pane_changed(self, event):
        """Refresh layout when the collapsible pane is expanded/collapsed."""
        self.Layout()

if __name__ == "__main__":
    app = wx.App(False)
    frame = CollapsiblePaneApp()
    frame.Show()
    app.MainLoop()
