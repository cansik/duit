from typing import Optional

import numpy as np
import pygfx as gfx
import wx
from wgpu.gui.wx import WgpuWidget

from duit.event.Event import Event


class WxGfxImageCanvas(WgpuWidget):
    """
    A custom widget for displaying and interacting with images using the pygfx library within a wxPython interface.
    Extends the WgpuWidget to enable GPU-accelerated rendering with image processing capabilities.
    """

    def __init__(self, parent, image: np.ndarray = None):
        """
        Initializes the WxGfxImageCanvas with an optional image, sets up the rendering scene, and binds resize events.

        Args:
            parent: The parent widget.
            image (np.ndarray, optional): Initial image to be displayed. Defaults to None.
        """
        super().__init__(parent)

        self._image: Optional[np.ndarray] = image

        self._update_texture_requested: bool = False
        self._resize_requested: bool = False
        self._reinit_image_requested: bool = False

        self.renderer = gfx.renderers.WgpuRenderer(self)
        self.scene = gfx.Scene()
        self.camera = gfx.OrthographicCamera()

        self.texture: Optional[gfx.Texture] = None
        self.gfx_image: Optional[gfx.Image] = None

        self.Bind(wx.EVT_SIZE, self.on_size)

        self.on_pointer_event: Event[gfx.PointerEvent] = Event()
        self.on_keyboard_event: Event[gfx.KeyboardEvent] = Event()
        self.on_wheel_event: Event[gfx.WheelEvent] = Event()

        self.request_draw(self._animate)

    @property
    def image(self) -> Optional[np.ndarray]:
        """
        Gets or sets the image displayed on the canvas.

        Returns:
            Optional[np.ndarray]: The current image displayed on the canvas, if any.
        """
        return self._image

    @image.setter
    def image(self, image: Optional[np.ndarray]):
        """
        Sets the image to be displayed on the canvas and flags the texture and camera for update.

        Args:
            image (Optional[np.ndarray]): New image to display, or None to clear the image.
        """
        if image is None:
            self._reinit_image_requested = True
        else:
            # Check if the two images have the same shape (update)
            if self._image.shape[0] != image.shape[0] or self._image.shape[1] != image.shape[1]:
                self._reinit_image_requested = True

        self._image = image
        self._update_texture_requested = True
        self._resize_requested = True  # Ensure camera updates when image changes

    def _animate(self):
        """
        Animation loop handler for updating and rendering the scene as needed.
        Triggers updates to texture and camera if flagged, and requests another frame for animation.
        """
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
        """
        Updates the texture used by the renderer to match the current image data.
        Creates and manages gfx.Texture and gfx.Image instances for rendering the image.
        """
        if self._reinit_image_requested:
            self._reinit_image_requested = False
            if self.gfx_image is not None:
                self.scene.remove(self.gfx_image)
                self.gfx_image = None
                self.texture = None

        if self._image is None:
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

            # add handlers
            self.gfx_image.add_event_handler(self.on_pointer_event,
                                             "pointer_down", "pointer_move", "pointer_up", "pointer_enter",
                                             "pointer_leave", "click", "double_click")
            self.gfx_image.add_event_handler(self.on_keyboard_event, "key_down", "key_up")
            self.gfx_image.add_event_handler(self.on_wheel_event, "wheel")

        self.texture.data[:] = self._image[:]
        self.texture.update_full()

    def _update_camera(self):
        """
        Updates the orthographic camera settings to maintain the correct aspect ratio of the displayed image
        relative to the widget size, centering the image in the display area.
        """
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
        """
        Event handler for widget resize events. Flags the canvas for resizing and processes the event.

        Args:
            event: The wxPython size event.
        """
        self._resize_requested = True
        event.Skip()
