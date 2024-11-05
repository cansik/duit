from typing import Optional

import numpy as np
import pygfx as gfx
import wx
from wgpu.gui.wx import WgpuWidget

from duit.event.Event import Event


class WxGfxImageCanvas(WgpuWidget):
    def __init__(self, parent, image: np.ndarray = None):
        super().__init__(parent)

        self._image: Optional[np.ndarray] = image

        self._update_texture_requested: bool = False
        self._resize_requested: bool = False

        self.renderer = gfx.renderers.WgpuRenderer(self)
        self.scene = gfx.Scene()
        self.camera = gfx.OrthographicCamera()

        self.texture: Optional[gfx.Texture] = None
        self.gfx_image: Optional[gfx.Image] = None

        self.Bind(wx.EVT_SIZE, self.on_size)

        self.on_mouse_event: Event[gfx.PointerEvent] = Event()

        self.request_draw(self._animate)

    @property
    def image(self) -> Optional[np.ndarray]:
        return self._image

    @image.setter
    def image(self, image: Optional[np.ndarray]):
        self._image = image
        self._update_texture_requested = True
        self._resize_requested = True  # Ensure camera updates when image changes

    def _animate(self):
        render_needed = self._update_texture_requested or self._resize_requested

        if self._update_texture_requested:
            self._update_texture()
            self._update_texture_requested = False

        if self._resize_requested:
            self._update_camera()
            self._resize_requested = False

        if render_needed:
            self.renderer.render(self.scene, self.camera)

        self.request_draw(self._animate)

    def _update_texture(self):
        if self._image is None:
            if self.gfx_image is not None:
                self.scene.remove(self.gfx_image)
                self.gfx_image = None
                self.texture = None
            return

        if self.texture is None:
            self.texture = gfx.Texture(self._image, dim=2)

        if self.gfx_image is None:
            self.gfx_image = gfx.Image(
                gfx.Geometry(grid=self.texture),
                gfx.ImageBasicMaterial(clim=(0, 255), pick_write=True),
            )

            self.scene.add(self.gfx_image)
            self.camera.local.scale_y = -1  # Flip image vertically

        self.texture.data[:] = self._image[:]
        self.texture.update_range((0, 0, 0), self._image.shape[:2] + (1,))

    def _update_camera(self):
        if self._image is None:
            return

        w_image, h_image = self._image.shape[1], self._image.shape[0]
        w_widget, h_widget = self.GetClientSize()

        # Compute the aspect ratios
        aspect_image = w_image / h_image
        aspect_widget = w_widget / h_widget

        # Adjust the camera width and height to fit the image within the widget, maintaining aspect ratio
        if aspect_widget > aspect_image:
            # Widget is wider than image aspect ratio
            self.camera.height = h_image
            self.camera.width = h_image * aspect_widget
        else:
            # Widget is taller than image aspect ratio
            self.camera.width = w_image
            self.camera.height = w_image / aspect_widget

        # Update camera position to center on the image
        self.camera.local.position = (w_image / 2, h_image / 2, self.camera.local.position[2])

        self.camera.update_projection_matrix()

    def on_size(self, event):
        self._resize_requested = True
        event.Skip()
