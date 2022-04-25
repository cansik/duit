import threading
import time
from typing import Optional

import numpy as np
import open3d.visualization.gui as gui

from duit.vision.ImagePreview import ImagePreview


class Open3dImagePreview(ImagePreview):
    def __init__(self, title: str = "Image Preview", width: int = 640, height: int = 480,
                 app: Optional[gui.Application] = None):
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
        if self._is_open:
            return

        super().open()

        def run_app():
            while self._is_open:
                self.app.run_one_tick()
                self.window.post_redraw()
                time.sleep(0.33)
            # self.app.run()

        # run app
        self.ui_thread = threading.Thread(target=run_app, daemon=True)
        self.ui_thread.start()

    def display(self, image: np.ndarray):
        pass

    def close(self):
        if not self._is_open:
            return

        self.app.quit()
        self.ui_thread.join(30)

    def set_window_size(self, width: int, height: int):
        print(self.window.size)

    def _on_layout(self, layout_context):
        content_rect = self.window.content_rect
        self.panel.frame = content_rect

    def _on_close(self):
        gui.Application.instance.quit()
