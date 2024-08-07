from typing import Optional

import numpy as np
import pygfx as gfx
import wx
from wgpu.gui.wx import WgpuWidget


class WxGfxImageCanvas(WgpuWidget):
    def __init__(self, parent, image: np.ndarray = None):
        super().__init__(parent)

        self._image: Optional[np.ndarray] = image

        self._update_texture_requested: bool = False
        self._update_projection_requested: bool = False

        self.renderer = gfx.renderers.WgpuRenderer(self)
        self.scene = gfx.Scene()
        self.camera = gfx.OrthographicCamera()

        self.texture: Optional[gfx.Texture] = None
        self.gfx_image: Optional[gfx.Image] = None

        self.Bind(wx.EVT_SIZE, self.on_size)

        self.request_draw(self._animate)

    @property
    def image(self) -> Optional[np.ndarray]:
        return self._image

    @image.setter
    def image(self, image: Optional[np.ndarray]):
        self._image = image
        self._update_texture_requested = True

    def _animate(self):
        render_needed = self._update_texture_requested or self._update_projection_requested

        if self._update_texture_requested:
            self._update_texture()
            self._update_texture_requested = False

        if self._update_projection_requested:
            self._update_projection()
            self._update_projection_requested = False

        if render_needed:
            self.renderer.render(self.scene, self.camera)
            self.request_draw()

    def _update_texture(self):
        if self._image is None:
            if self.gfx_image is not None:
                self.scene.remove(self.gfx_image)
                self.gfx_image = None
                self.texture = None
            return

        h, w = self._image.shape[:2]

        if self.texture is None:
            self.texture = gfx.Texture(self._image, dim=2)

        if self.gfx_image is None:
            self.gfx_image = gfx.Image(
                gfx.Geometry(grid=self.texture),
                gfx.ImageBasicMaterial(clim=(0, 255)),
            )

            self.scene.add(self.gfx_image)

            self.camera.show_object(self.scene, view_dir=(0, 0, -1))
            self.camera.local.scale_y = -1

        self.texture.data[:] = self._image[:]
        self.texture.update_range((0, 0, 0), (w, h, 1))

    def on_size(self, event):
        self._update_projection_requested = True

    def _update_projection(self):
        size = self.GetClientSize()
        aspect_ratio = size.width / size.height
        self.camera.left = -size.width / 2
        self.camera.right = size.width / 2
        self.camera.top = size.height / 2
        self.camera.bottom = -size.height / 2
        self.camera.update_projection_matrix()
