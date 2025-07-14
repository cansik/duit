from AppKit import NSWorkspace
from Quartz import (
    CGWindowListCopyWindowInfo,
    kCGWindowListOptionOnScreenOnly,
    kCGNullWindowID,
    CGMainDisplayID,
    CGDisplayPixelsHigh,
)

# Default insets to strip off the frame decoration:
#   top: title-bar height (≈22px), bottom/left/right: 1px border
DEFAULT_DECOR_INSETS = {
    "top": 28,
    "bottom": 2,
    "left": 2,
    "right": 2,
}


def get_foremost_window_bounds(include_border: bool = True,
                               decor_insets: dict = None) -> dict:
    """
    Returns the bounds of the frontmost (active) window on macOS, in a
    top-left origin coordinate system.

    :param include_border: if False, will inset the rect by decor_insets
    :param decor_insets: dict with keys 'top','bottom','left','right'
                          to strip from the full window frame
    :returns: dict with keys 'x','y','width','height'
    :raises RuntimeError: if no frontmost window could be found
    """
    # ——————————————————————
    # 1) Get PID of the frontmost app
    ws = NSWorkspace.sharedWorkspace()
    app = ws.frontmostApplication()
    pid = app.processIdentifier()

    # ——————————————————————
    # 2) Fetch on-screen windows; pick the layer-0 window for that PID
    options = kCGWindowListOptionOnScreenOnly
    wins = CGWindowListCopyWindowInfo(options, kCGNullWindowID)
    for win in wins:
        if win.get("kCGWindowOwnerPID") == pid and win.get("kCGWindowLayer", 0) == 0:
            bounds = win.get("kCGWindowBounds")
            break
    else:
        raise RuntimeError(f"No frontmost window found for PID {pid}")

    # ——————————————————————
    # 3) Quartz is bottom-origin; convert to top-origin
    screen_h = CGDisplayPixelsHigh(CGMainDisplayID())
    x = int(bounds["X"])
    w = int(bounds["Width"])
    h = int(bounds["Height"])
    y = int(screen_h - bounds["Y"] - h)

    rect = {"x": x, "y": y, "width": w, "height": h}

    # ——————————————————————
    # 4) Optionally strip off the decoration insets
    if not include_border:
        inset = decor_insets or DEFAULT_DECOR_INSETS
        rect = {
            "x": rect["x"] + inset["left"],
            "y": rect["y"] + inset["top"],
            "width": rect["width"] - (inset["left"] + inset["right"]),
            "height": rect["height"] - (inset["top"] + inset["bottom"]),
        }

    return rect
