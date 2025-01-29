import time

import wx
import wx.adv

from duit.ui.wx.WxUtils import is_dark_mode


class WxToggleSwitch(wx.CheckBox):
    """
    A custom toggle switch widget built on top of wx.CheckBox to provide a modern UI appearance
    resembling a switch with on and off states.

    This toggle switch includes animations, customizable colors, and support for both light and dark modes.
    """

    def __init__(
            self,
            parent: wx.Window,
            id: int = wx.ID_ANY,
            label: str = "",
            value: bool = False,
            on_color: wx.Colour = wx.Colour(0, 122, 255),
            size: wx.Size = wx.Size(40, 20),
            style: int = 0
    ):
        """
        Initializes the WxToggleSwitch with a given parent window, appearance settings, and value state.

        Args:
            parent (wx.Window): The parent window for this widget.
            id (int, optional): The identifier for the widget. Defaults to wx.ID_ANY.
            label (str, optional): The label displayed alongside the switch. Defaults to an empty string.
            value (bool, optional): The initial value (checked state) of the switch. Defaults to False.
            on_color (wx.Colour, optional): The color used when the switch is in the 'on' state. Defaults to wx.Colour(0, 122, 255).
            size (wx.Size, optional): The size of the switch. Defaults to wx.Size(50, 25).
            style (int, optional): Additional style flags. Defaults to 0.
        """
        super().__init__(parent, id, label=label, style=style)
        self._value = value
        self._on_color = on_color
        self._is_dark_mode = is_dark_mode()
        self._off_color = wx.Colour(80, 80, 80) if self._is_dark_mode else wx.Colour(200, 200, 200)
        self._switch_radius = size.GetHeight() // 2

        # Correct the initial switch position based on value
        self._switch_position = (
            size.GetWidth() - self._switch_radius if self._value else self._switch_radius
        )

        self.SetMinSize(size)
        self.SetMaxSize(size)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnToggle)
        self.Bind(wx.EVT_LEFT_DCLICK, self.OnToggle)
        self.Bind(wx.EVT_SIZE, self.OnResize)

        self._animation_duration = 100  # milliseconds
        self.SetValue(value)  # Initialize the state

    def GetValue(self) -> bool:
        """
        Retrieves the current state (checked/unchecked) of the toggle switch.

        Returns:
            bool: The current state of the toggle switch.
        """
        return self.IsChecked()

    def SetValue(self, value: bool) -> None:
        """
        Sets the state (checked/unchecked) of the toggle switch and refreshes its appearance.

        Args:
            value (bool): The new state of the toggle switch.
        """
        self._value = value
        super().SetValue(value)
        self.Refresh()  # Redraw to update appearance

    def SetOnColor(self, color: wx.Colour) -> None:
        """
        Sets the color used when the switch is in the 'on' state.

        Args:
            color (wx.Colour): The color to use for the 'on' state.
        """
        self._on_color = color
        self.Refresh()

    def OnPaint(self, event: wx.PaintEvent) -> None:
        """
        Handles the paint event to draw the toggle switch, including its background
        and toggle circle, based on the current state.
        """
        width, height = self.GetSize()
        dc = wx.BufferedPaintDC(self)
        dc.Clear()  # Clear previous contents

        gc = wx.GraphicsContext.Create(dc)

        # Draw background with rounded rectangle
        gc.SetBrush(gc.CreateBrush(wx.Brush(self._on_color if self._value else self._off_color)))
        path = gc.CreatePath()
        path.AddRoundedRectangle(0, 0, width, height, self._switch_radius)
        gc.FillPath(path)

        # Draw toggle circle
        toggle_color = wx.Colour(255, 255, 255) if not self._is_dark_mode else wx.Colour(200, 200, 200)
        gc.SetBrush(gc.CreateBrush(wx.Brush(toggle_color)))
        gc.DrawEllipse(self._switch_position - self._switch_radius, height // 2 - self._switch_radius,
                       self._switch_radius * 2, self._switch_radius * 2)

    def OnToggle(self, event: wx.MouseEvent) -> None:
        """
        Toggles the state of the switch when a left mouse button down or double-click event occurs,
        triggers an animation, and posts a wx.CommandEvent to signal the state change.
        """
        self._value = not self._value
        self.SetValue(self._value)
        self.AnimateToggle()
        # Optionally, trigger the checkbox event handlers
        evt = wx.CommandEvent(wx.EVT_CHECKBOX.typeId, self.GetId())
        evt.SetInt(self._value)
        wx.PostEvent(self, evt)

    def OnResize(self, event):
        """
        Handles the resize event to ensure the switch respects its minimum and maximum size constraints.
        """
        size = self.GetSize()
        min_size = self.GetMinSize()
        max_size = self.GetMaxSize()

        # Enforce min and max size
        new_width = min(max(size.GetWidth(), min_size.GetWidth()), max_size.GetWidth())
        new_height = min(max(size.GetHeight(), min_size.GetHeight()), max_size.GetHeight())
        self.SetSize(wx.Size(new_width, new_height))
        event.Skip()

    def AnimateToggle(self) -> None:
        """
        Animates the movement of the toggle switch circle to create a smooth transition effect
        between 'on' and 'off' states.
        """
        start_time = time.time()
        start_pos = self._switch_position
        end_pos = self.GetSize().GetWidth() - self._switch_radius if self._value else self._switch_radius

        def animate():
            nonlocal start_time, start_pos, end_pos
            elapsed = (time.time() - start_time) * 1000  # milliseconds
            t = min(1, elapsed / self._animation_duration)

            new_pos = int(start_pos + (end_pos - start_pos) * t)
            self._switch_position = new_pos
            self.Refresh()

            if t < 1:
                wx.CallLater(10, animate)

        animate()

    def DoGetBestSize(self) -> wx.Size:
        """
        Returns the best size for the toggle switch based on its minimum size.

        Returns:
            wx.Size: The best size for the widget.
        """
        return self.GetMinSize()
