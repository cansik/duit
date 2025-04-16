import struct
from queue import Queue

import cv2
import numpy as np
from nicegui.element import Element


class VideoStream(Element, component='video_stream.js'):
    """
    A NiceGUI component that streams raw RGBA frames via WebSocket to a <canvas>.

    Use `vs = VideoStream()` in your UI to add it to the page,
    and call `vs.stream(frame)` to send new OpenCV frames.
    """
    # class-level queue: always holds latest frame
    frame_queue: Queue[bytes] = Queue(maxsize=1)

    def __init__(self, endpoint: str = '/ws/stream'):
        super().__init__()
        # pass endpoint to the Vue component
        self._props['endpoint'] = endpoint

    def stream(self, frame: np.ndarray) -> None:
        """
        Push a new BGR OpenCV frame to the internal queue.
        Converts to RGBA, prepends width/height header.
        """
        # convert BGR to RGBA
        rgba = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        h, w, _ = rgba.shape
        body = rgba.tobytes()
        # pack width & height as two big-endian uint32s
        header = struct.pack('>II', w, h)
        buf = header + body
        # replace any old frame
        try:
            VideoStream.frame_queue.put(buf, block=False)
        except:
            VideoStream.frame_queue.get(block=False)
            VideoStream.frame_queue.put(buf, block=False)
