from typing import Optional

import cv2
import numpy as np
import pygfx as gfx
import wx
from wgpu.gui.wx import WgpuWidget


class WxGfxImageCanvas(WgpuWidget):
    def __init__(self, parent, image: np.ndarray = None):
        super().__init__(parent)

        self.renderer = gfx.renderers.WgpuRenderer(self)
        self.scene = gfx.Scene()
        self.camera = gfx.OrthographicCamera()

        self.texture: Optional[gfx.Texture] = None
        self.geometry: Optional[gfx.Geometry] = None
        self.material: Optional[gfx.Material] = None
        self.mesh: Optional[gfx.Mesh] = None

        self.Bind(wx.EVT_SIZE, self.on_size)

    @property
    def image(self) -> np.ndarray:
        return self.texture.image

    @image.setter
    def image(self, image: np.ndarray):
        h, w = image.shape[:2]

        if self.texture is None:
            self.texture = gfx.Texture(image, dim=2)

        if self.geometry is None:
            self.geometry = gfx.plane_geometry(w, h)

        if self.material is None:
            self.material = gfx.MeshBasicMaterial(map=self.texture)

        if self.mesh is None:
            self.mesh = gfx.Mesh(self.geometry, self.material)
            self.scene.add(self.mesh)

        self.texture.image = image
        self.texture.update_range((0, 0, 0), (1, 1, 1))
        self.geometry = gfx.plane_geometry(1, h / w)
        self.mesh.geometry = self.geometry

        self.refresh_scene()

    def refresh_scene(self):
        def update():
            self.renderer.render(self.scene, self.camera)
            self.request_draw()

        wx.CallAfter(update)

    def on_size(self, event):
        wx.CallAfter(self.update_projection)

    def update_projection(self):
        size = self.GetClientSize()
        aspect_ratio = size.width / size.height
        self.camera.left = -size.width / 2
        self.camera.right = size.width / 2
        self.camera.top = size.height / 2
        self.camera.bottom = -size.height / 2
        self.camera.update_projection_matrix()
        self.refresh_scene()
