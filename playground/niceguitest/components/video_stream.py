import asyncio
import struct
from queue import Queue

import cv2
import numpy as np
from fastapi import WebSocket
from nicegui import app
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
        self._register()

    def stream(self, frame: np.ndarray) -> None:
        """
        Push a new BGR OpenCV frame to the internal queue.
        Converts to RGBA, prepends width/height header.
        """
        # convert BGR to RGBA
        rgba = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        # rgba = cv2.resize(rgba, (640, 480))
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

    def _register(self):
        def get_event_loop():
            # helper to avoid lint complaints
            return asyncio.get_event_loop()

        @app.websocket('/ws/stream')
        async def ws_stream(websocket: WebSocket):
            """
            Accepts WebSocket connections and sends raw RGBA frames as binary messages.
            """
            await websocket.accept()
            loop = get_event_loop()
            print('ws started')
            while True:
                buf: bytes = await loop.run_in_executor(None, VideoStream.frame_queue.get)
                await websocket.send_bytes(buf)
