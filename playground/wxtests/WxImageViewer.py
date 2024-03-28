import threading
import time

import cv2
import wx
import numpy as np


class WxImageViewer(wx.Panel):
    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.NO_BORDER):
        super().__init__(parent, id, pos, size, style)
        self.image = None
        self.bitmap = None
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)

    def set_image(self, image: np.ndarray):
        self.image = image
        self.update_bitmap()
        self.Refresh()

    def update_bitmap(self):
        if self.image is not None:
            height, width = self.image.shape[:2]
            if self.bitmap is None or self.bitmap.GetSize() != (width, height):
                # Convert to wx.Image to use for Bitmap creation, allows for easy resizing
                self.bitmap = wx.Bitmap.FromBuffer(width, height, self.image)

    def OnPaint(self, event):
        if self.bitmap is not None:
            dc = wx.BufferedPaintDC(self)
            self.draw_bitmap_centered(dc)

    def draw_bitmap_centered(self, dc):
        width, height = self.GetClientSize()
        img_width, img_height = self.bitmap.GetSize()

        # Scale the image to fit within the control, maintaining aspect ratio
        img_aspect = img_width / img_height
        ctrl_aspect = width / height
        scale = min(width / img_width, height / img_height)
        new_width = round(img_width * scale)
        new_height = round(img_height * scale)

        # Calculate position to center the image
        pos_x = int((width - new_width) / 2)
        pos_y = int((height - new_height) / 2)

        # Convert bitmap to image for scaling, then back to bitmap
        image = self.bitmap.ConvertToImage()
        scaled_image = image.Scale(new_width, new_height, wx.IMAGE_QUALITY_HIGH)
        scaled_bitmap = wx.Bitmap(scaled_image)

        # Draw the image
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()
        dc.DrawBitmap(scaled_bitmap, pos_x, pos_y, True)

    def OnSize(self, event):
        self.Refresh()
        event.Skip()
