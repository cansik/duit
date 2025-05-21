from queue import Queue

import cv2
import numpy as np
from fastapi import Request
from fastapi.responses import StreamingResponse
from nicegui import app
from nicegui.element import Element


class OpencvViewer(Element, component='opencv_viewer.js'):
    """
    NiceGUI component for MJPEG streaming.

    Usage:
        vs = VideoStream(endpoint='/mjpeg', quality=80)
        vs.stream(frame)  # push OpenCV frame into stream
    """
    # shared, size-1 queue to always hold latest JPEG bytes
    frame_queue: Queue[bytes] = Queue(maxsize=1)

    def __init__(self,
                 endpoint: str = '/mjpeg',
                 quality: int = 80):
        super().__init__()
        # tell Vue the URL to request
        self._props['endpoint'] = endpoint
        self.endpoint = endpoint
        self.quality = quality

        self._register()

    def stream(self, frame: np.ndarray) -> None:
        """
        Encode a BGR OpenCV frame to JPEG and enqueue it.
        Drops old frames to avoid backlog.
        """
        success, buf = cv2.imencode('.jpg', frame,
                                    [cv2.IMWRITE_JPEG_QUALITY, self.quality])
        if not success:
            return
        data = buf.tobytes()
        # replace old frame atomically
        try:
            OpencvViewer.frame_queue.put(data, block=False)
        except:
            OpencvViewer.frame_queue.get(block=False)
            OpencvViewer.frame_queue.put(data, block=False)

    def _register(self):
        @app.get(self.endpoint)
        async def mjpeg_endpoint(request: Request):
            """
            Streams multipart MJPEG at /mjpeg.
            """
            boundary = "--frame"

            async def generator():
                while True:
                    # if client disconnects, exit
                    if await request.is_disconnected():
                        break
                    # get next frame (blocking)
                    frame = OpencvViewer.frame_queue.get()
                    # build multipart chunk
                    yield (
                            boundary.encode() + b"\r\n"
                                                b"Content-Type: image/jpeg\r\n"
                                                b"Content-Length: " + str(len(frame)).encode() + b"\r\n\r\n" +
                            frame + b"\r\n"
                    )

            return StreamingResponse(generator(),
                                     media_type="multipart/x-mixed-replace; boundary=frame")
