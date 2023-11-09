import threading
import time
from typing import Optional

import numpy as np
import open3d.visualization.gui as gui

from duit.vision.ImagePreview import ImagePreview


class Open3dImagePreview(ImagePreview):
    """
    Image preview implementation using Open3D's GUI framework.

    Args:
        title (str): The title of the image preview window.
        width (int): The width of the image preview window.
        height (int): The height of the image preview window.
        app (Optional[gui.Application]): An optional Open3D GUI application instance. If not provided, a new one will be created.
    """

    def __init__(self, title: str = "Image Preview", width: int = 640, height: int = 480,
                 app: Optional[gui.Application] = None):
        """
        Initialize the Open3dImagePreview instance.

        Args:
            title (str): The title of the image preview window.
            width (int): The width of the image preview window.
            height (int): The height of the image preview window.
            app (Optional[gui.Application]): An optional Open3D GUI application instance. If not provided, a new one will be created.
        """
        super().__init__(title, width, height)

        # get and init app
        if app is None:
            self.app: gui.Application = gui.Application.instance
            self.app.initialize()
        else:
            self.app = app

        self.window: gui.Window = self.app.create_window(title, width, height)
        self.window.set_on_layout(self._on_layout)
        self.window.set_on_close(self._on_close)

    def open(self):
        """
        Open the image preview window.

        Args:
            None
        """
        if self._is_open:
            return

        super().open()

        def run_app():
            while self._is_open:
                self.app.run_one_tick()
                self.window.post_redraw()
                time.sleep(0.33)

        # run app
        self.ui_thread = threading.Thread(target=run_app, daemon=True)
        self.ui_thread.start()

    def display(self, image: np.ndarray):
        """
        Display an image in the Open3D image preview window. (Not implemented)

        Args:
            image (np.ndarray): The image to be displayed in the preview window.

        Raises:
            NotImplementedError: This method is not implemented in this subclass.
        """
        raise NotImplementedError("Display method is not implemented in Open3dImagePreview.")

    def close(self):
        """
        Close the image preview window.

        Args:
            None
        """
        if not self._is_open:
            return

        self.app.quit()
        self.ui_thread.join(30)

    def set_window_size(self, width: int, height: int):
        """
        Set the size of the image preview window.

        Args:
            width (int): The new width of the window.
            height (int): The new height of the window.
        """
        print(self.window.size)

    def _on_layout(self, layout_context):
        content_rect = self.window.content_rect
        self.panel.frame = content_rect

    def _on_close(self):
        gui.Application.instance.quit()
