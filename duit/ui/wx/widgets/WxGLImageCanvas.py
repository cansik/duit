from typing import Optional, Tuple

import numpy as np
import wx
import wx.glcanvas as glcanvas
from OpenGL.GL import *
from OpenGL.GLUT import *


class WxGLImageCanvas(glcanvas.GLCanvas):
    TEX_COORDINATES = [
        (0.0, 0.0),
        (1.0, 0.0),
        (1.0, 1.0),
        (0.0, 1.0)
    ]

    def __init__(self, parent, image: Optional[np.ndarray] = None, fps: float = 60.0):
        attribs = (glcanvas.WX_GL_RGBA, glcanvas.WX_GL_DOUBLEBUFFER, glcanvas.WX_GL_DEPTH_SIZE, 24)
        super(WxGLImageCanvas, self).__init__(parent, attribList=attribs)

        self.context = glcanvas.GLContext(self)
        self.texture = None
        self.image_size = (0, 0)
        self.canvas_aspect_ratio = 1.0
        self.image_aspect_ratio = 1.0

        self._image: Optional[np.ndarray] = image
        self._redraw_requested: bool = True

        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_SIZE, self.on_size)

        # Timer for steady texture updates
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_timer, self.timer)
        self.timer.Start(1000 / fps)

    @property
    def image(self) -> Optional[np.ndarray]:
        return self._image

    @image.setter
    def image(self, value: Optional[np.ndarray]):
        self._image = value
        if value is not None:
            self.image_aspect_ratio = value.shape[1] / value.shape[0]
        self._redraw_requested = True

    def request_redraw(self):
        self._redraw_requested = True

    def update_image(self):
        if not self._redraw_requested or self._image is None:
            return

        self._redraw_requested = False

        image = self._image
        self.image_size = image.shape[1::-1]  # (width, height)
        image = np.flipud(image)  # OpenGL expects the data flipped vertically
        if self.texture is None:
            self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, self.image_size[0], self.image_size[1], 0, GL_RGB, GL_UNSIGNED_BYTE,
                     image)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        self.Refresh()

    def on_paint(self, event):
        dc = wx.PaintDC(self)
        self.SetCurrent(self.context)
        if not self.texture:
            return
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture)

        # Adjust drawing coordinates based on aspect ratios to maintain the image's aspect ratio and center it
        if self.canvas_aspect_ratio > self.image_aspect_ratio:
            scale = self.image_aspect_ratio / self.canvas_aspect_ratio
            vertices = [(-scale, -1), (scale, -1), (scale, 1), (-scale, 1)]
        else:
            scale = self.canvas_aspect_ratio / self.image_aspect_ratio
            vertices = [(-1, -scale), (1, -scale), (1, scale), (-1, scale)]

        glBegin(GL_QUADS)
        for i, (x, y) in enumerate(vertices):
            glTexCoord2f(*self.TEX_COORDINATES[i])
            glVertex2f(x, y)
        glEnd()

        glFlush()
        self.SwapBuffers()

    def on_size(self, event):
        size = self.GetClientSize()
        self.canvas_aspect_ratio = size.width / size.height
        self.SetCurrent(self.context)
        glViewport(0, 0, size.width, size.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-1, 1, -1, 1, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        self.Refresh()

    def on_timer(self, event):
        self.update_image()

    def canvas_to_image_coordinates(self, canvas_x: int, canvas_y: int) -> Optional[Tuple[float, float]]:
        """
        Convert canvas coordinates (x, y) to image coordinates.
        :param canvas_x: X coordinate on the canvas.
        :param canvas_y: Y coordinate on the canvas.
        :return: Image coordinates (x, y) or None if coordinates are not on the image.
        """
        # Check if canvas coordinates are within the bounds of the image
        if not (0 <= canvas_x < self.GetClientSize().GetWidth() and 0 <= canvas_y < self.GetClientSize().GetHeight()):
            return None

        # Calculate the aspect ratio scale
        if self.canvas_aspect_ratio > self.image_aspect_ratio:
            scale = self.image_aspect_ratio / self.canvas_aspect_ratio
        else:
            scale = self.canvas_aspect_ratio / self.image_aspect_ratio

        # Map canvas coordinates to image coordinates
        image_x = (canvas_x / self.GetClientSize().GetWidth()) * 2 * scale - scale
        image_y = ((self.GetClientSize().GetHeight() - canvas_y) / self.GetClientSize().GetHeight()) * 2 * scale - scale

        return image_x, image_y
