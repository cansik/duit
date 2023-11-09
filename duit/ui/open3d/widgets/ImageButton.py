from typing import Callable, Optional

from open3d.cpu.pybind.visualization.gui import Widget, MouseEvent
from open3d.visualization import gui


class ImageButton(gui.ImageWidget):
    def __init__(self, *args, **kwargs):
        """
        Constructor for ImageButton class.

        Args:
            *args: Positional arguments passed to the parent class constructor.
            **kwargs: Keyword arguments passed to the parent class constructor.

        This class inherits from the `gui.ImageWidget` class and adds the ability to set an event handler for a button click.

        """
        super().__init__(*args, **kwargs)

        self.set_on_mouse(self._handle_mouse_event)
        self._event_handler: Optional[Callable[[], None]] = None

    def set_on_clicked(self, event: Callable[[], None]):
        """
        Set an event handler for a button click.

        Args:
            event (Callable[[], None]): The event handler function to be called when the button is clicked.

        """
        self._event_handler = event

    def _handle_mouse_event(self, e: MouseEvent) -> Widget.EventCallbackResult:
        """
        Handle mouse events for the button.

        Args:
            e (MouseEvent): The mouse event object.

        Returns:
            Widget.EventCallbackResult: The result of the event handling.

        This method is called when mouse events occur on the button. It checks for button clicks and triggers the
        associated event handler if defined.

        """
        if e.type == MouseEvent.BUTTON_DOWN:
            if self._event_handler is not None:
                self._event_handler()

        return Widget.EventCallbackResult.CONSUMED
