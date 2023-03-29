from typing import Callable, Optional

from open3d.cpu.pybind.visualization.gui import Widget, MouseEvent
from open3d.visualization import gui


class ImageButton(gui.ImageWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_on_mouse(self._handle_mouse_event)
        self._event_handler: Optional[Callable[[], None]] = None

    def set_on_clicked(self, event: Callable[[], None]):
        self._event_handler = event

    def _handle_mouse_event(self, e: MouseEvent) -> Widget.EventCallbackResult:
        print(e.x)

        if e.type == MouseEvent.BUTTON_DOWN:
            if self._event_handler is not None:
                self._event_handler()

        return Widget.EventCallbackResult.CONSUMED
