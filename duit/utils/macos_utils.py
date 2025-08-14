import os
from pathlib import Path

from duit.utils import os_utils


@os_utils.require_macos
def disable_app_nap_on_macos():
    """
    Disables App Nap on macOS to prevent the application from being throttled
    when it is not in the foreground.

    This function checks if the operating system is macOS and uses the
    `appnope` module to disable App Nap for the current process.
    """
    import appnope

    # disable App Nap for the rest of your process
    appnope.nope()


@os_utils.require_macos
def set_app_icon(path: str | os.PathLike):
    """
    Sets the application icon in the macOS Dock.

    This function loads an image from the provided file path and sets it as the
    application's icon in the macOS Dock using the AppKit framework.

    :param path: Path to the image file to be used as the Dock icon. Must be a valid image.

    :raises FileNotFoundError: If the provided icon path does not exist.
    :raises ImportError: If the required pyobjc modules are not installed.
    """
    try:
        from AppKit import NSApplication, NSApp, NSImage
    except ImportError:
        raise ImportError(
            "Could not import AppKit from pyobjc. Please install with:\npip install pyobjc-core pyobjc-framework-Cocoa")

    icon_path = Path(path)
    if not icon_path.exists():
        raise FileNotFoundError(f"Could not find icon at {icon_path}")

    app = NSApplication.sharedApplication()
    icon = NSImage.alloc().initByReferencingFile_(str(icon_path.absolute()))

    if icon is not None and icon.size().width > 0:
        NSApp.setApplicationIconImage_(icon)

    # if it loaded OK, swap in the Dock icon
    if icon is not None and icon.size().width > 0:
        app.setApplicationIconImage_(icon)
    else:
        print("Failed to load icon:", icon_path)


@os_utils.require_macos
def set_dock_badge_label(label: str):
    """
    Sets a badge label on the macOS Dock icon.

    This function updates the application's Dock icon with a badge label using
    the AppKit framework. Useful for showing notifications or counts.

    :param label: The string label to display as a badge on the Dock icon.

    :raises ImportError: If the required pyobjc modules are not installed.
    """
    try:
        from AppKit import NSApplication
        from Foundation import NSProcessInfo
    except ImportError:
        raise ImportError(
            "Could not import AppKit/Foundation from pyobjc. Install with:\npip install pyobjc-core pyobjc-framework-Cocoa"
        )

    # Ensure there is a shared NSApplication
    app = NSApplication.sharedApplication()

    dock = app.dockTile()
    dock.setBadgeLabel_(label)
    dock.display()
