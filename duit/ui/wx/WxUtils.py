import os

import wx

MAX_INT32 = 2 ** 31 - 1
MIN_INT32 = 2 ** 31 * -1


def enable_high_dpi_mode():
    if os.name != "nt":
        return

    try:
        from ctypes import OleDLL

        # Turn on high-DPI awareness to make sure rendering is sharp on big
        # monitors with font scaling enabled.
        OleDLL("shcore").SetProcessDpiAwareness(1)

    except AttributeError:
        pass

    except OSError:
        # exc.winerror is often E_ACCESSDENIED (-2147024891/0x80070005).
        # This occurs after the first run, when the parameter is reset in the
        # executable's manifest and then subsequent calls raise this exception
        # See last paragraph of Remarks at
        # [https://msdn.microsoft.com/en-us/library/dn302122(v=vs.85).aspx](https://msdn.microsoft.com/en-us/library/dn302122(v=vs.85).aspx)
        pass


def is_dark_mode() -> bool:
    """
    Determines if the current system appearance is in dark mode.

    Returns:
        bool: True if the system is in dark mode, False otherwise.
    """
    if hasattr(wx, "SystemSettings") and hasattr(wx.SystemSettings, "GetAppearance"):
        return wx.SystemSettings().GetAppearance().IsDark()
    elif wx.Platform == "__WXMAC__":
        try:
            return wx.SystemAppearance().IsDark()
        except TypeError:
            return False
    else:
        return False
