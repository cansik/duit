# Example usage
import threading
import time

import cv2
import wx

from duit.ui.wx.widgets.WxGLImageCanvas import WxGLImageCanvas

if __name__ == "__main__":
    app = wx.App(False)
    frame = wx.Frame(None, title='WxImageViewer Demo', size=(800, 600))
    image_canvas = WxGLImageCanvas(frame)
    frame.Show()


    def playback_loop():
        cap = cv2.VideoCapture("/Users/cansik/Downloads/1093662-hd_1920_1080_30fps.mp4")

        success = True
        while success:
            success, image = cap.read()

            if not success:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                success = True
                continue

            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            image_canvas.image = image

        cap.release()


    threading.Thread(target=playback_loop, daemon=True).start()
    app.MainLoop()
