from typing import Optional

import wx

from duit.ui.wx.WxUtils import is_dark_mode

# Define a custom event type that mimics wxEVT_COLLAPSIBLEPANE_CHANGED
wxEVT_COLLAPSIBLEPANE_CHANGED = wx.NewEventType()
EVT_COLLAPSIBLEPANE_CHANGED = wx.PyEventBinder(wxEVT_COLLAPSIBLEPANE_CHANGED, 1)


class CollapsiblePaneEvent(wx.PyCommandEvent):
    """Event sent when the collapsible pane is expanded or collapsed."""

    def __init__(self, etype=wxEVT_COLLAPSIBLEPANE_CHANGED, eid=0):
        super().__init__(etype, eid)
        self._collapsed = True

    def SetCollapsed(self, c: bool) -> None:
        self._collapsed = c

    def IsCollapsed(self) -> bool:
        return self._collapsed

    def IsExpanded(self) -> bool:
        return not self._collapsed


class WxCollapsiblePane(wx.Panel):
    """
    A custom collapsible pane that behaves similarly to wx.CollapsiblePane.

    :param parent: The parent window.
    :param id: Window identifier.
    :param label: The label displayed on the collapsible pane header.
    :param pos: The position of the window.
    :param size: The size of the window.
    :param style: The style flags.
    :param name: The name of the window.
    :param content_padding: Extra left padding for nested content.
    :param font_size: Font size for the header text and icon.
    """

    def __init__(
            self,
            parent: wx.Window,
            id: int = wx.ID_ANY,
            label: str = "Collapsible Pane",
            pos: wx.Point = wx.DefaultPosition,
            size: wx.Size = wx.DefaultSize,
            style: int = wx.TAB_TRAVERSAL,
            name: str = "WxCollapsiblePane",
            content_padding: int = 15,
            font_size: int = 14
    ):
        super().__init__(parent, id=id, pos=pos, size=size, style=style, name=name)

        self._label_text = label
        self._is_collapsed = True
        self._is_dark_mode = is_dark_mode()

        # Main sizer
        self._sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self._sizer)

        # Header (toggle button + label) panel
        self._header_panel = wx.Panel(self)
        self._header_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Toggle icon, simulating arrow
        self._toggle_icon = wx.StaticText(
            self._header_panel, label=self._get_arrow_label(), style=wx.ALIGN_CENTER_VERTICAL
        )
        self._header_label = wx.StaticText(self._header_panel, label=self._label_text)

        # Set font of icon and header label
        font: wx.Font = self._toggle_icon.GetFont()
        font.SetPointSize(font_size)
        font.SetWeight(wx.FONTWEIGHT_BOLD)

        # Apply the modified font
        self._toggle_icon.SetFont(font)
        self._header_label.SetFont(font)

        # Set up header background
        self._header_panel.SetBackgroundColour(self._get_header_color())

        # Bind clicks on header
        self._header_panel.Bind(wx.EVT_LEFT_DOWN, self._on_header_click)
        self._header_panel.Bind(wx.EVT_LEFT_DCLICK, self._on_header_click)
        self._toggle_icon.Bind(wx.EVT_LEFT_DOWN, self._on_header_click)
        self._toggle_icon.Bind(wx.EVT_LEFT_DCLICK, self._on_header_click)
        self._header_label.Bind(wx.EVT_LEFT_DOWN, self._on_header_click)
        self._header_label.Bind(wx.EVT_LEFT_DCLICK, self._on_header_click)

        # Add header items to sizer
        self._header_sizer.Add(self._toggle_icon, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self._header_sizer.Add(self._header_label, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self._header_panel.SetSizer(self._header_sizer)

        self._sizer.Add(self._header_panel, 0, wx.EXPAND)

        # Content panel, initially hidden
        self._content_panel = wx.Panel(self)
        self._content_sizer = wx.BoxSizer(wx.VERTICAL)
        self._content_panel.SetSizer(self._content_sizer)

        # self._sizer.Add(self._content_panel, 1, wx.EXPAND)
        self._sizer.Add(self._content_panel, 1, wx.EXPAND | wx.LEFT, content_padding)
        self._content_panel.Hide()

        self.Layout()

    def _get_header_color(self) -> wx.Colour:
        """Determine header background color based on dark mode."""
        return wx.Colour(60, 60, 60) if self._is_dark_mode else wx.Colour(220, 220, 220)

    def _get_arrow_label(self) -> str:
        """Return the arrow label based on collapsed/expanded state."""
        return "▶" if self._is_collapsed else "▼"

    def _fire_collapsiblepane_event(self) -> None:
        """Fire a collapsible pane changed event."""
        evt = CollapsiblePaneEvent(eid=self.GetId())
        evt.SetEventObject(self)
        evt.SetCollapsed(self._is_collapsed)
        self.GetEventHandler().ProcessEvent(evt)

    def _on_header_click(self, event: Optional[wx.Event]) -> None:
        self.Collapse(not self._is_collapsed)

    def GetPane(self) -> wx.Window:
        """Return the content panel (like wx.CollapsiblePane.GetPane)."""
        return self._content_panel

    def Collapse(self, collapse: bool = True) -> None:
        """Collapse or expand the pane."""
        if self._is_collapsed == collapse:
            # No change in state
            return
        self._is_collapsed = collapse

        # Update arrow
        self._toggle_icon.SetLabel(self._get_arrow_label())

        if self._is_collapsed:
            self._content_panel.Hide()
        else:
            self._content_panel.Show()

        self.Layout()
        # Force parent to re-layout if needed
        if self.GetParent():
            self.GetParent().Layout()

        # Fire event
        self._fire_collapsiblepane_event()

    def Expand(self) -> None:
        """Expand the pane."""
        self.Collapse(False)

    def IsExpanded(self) -> bool:
        """Check if the pane is expanded."""
        return not self._is_collapsed

    def IsCollapsed(self) -> bool:
        """Check if the pane is collapsed."""
        return self._is_collapsed

    def SetLabel(self, label: str) -> None:
        """Set the label of the collapsible pane."""
        self._label_text = label
        self._header_label.SetLabel(label)

    def GetLabel(self) -> str:
        """Get the label of the collapsible pane."""
        return self._label_text

    def GetControlSizer(self) -> wx.Sizer:
        """Return the sizer used for the content panel."""
        return self._content_sizer
