import asyncio
from queue import Queue, Full

import cv2
import numpy as np
from fastapi import Request
from fastapi.responses import StreamingResponse
from nicegui import app
from nicegui.element import Element


class OpencvViewer(Element, component='opencv_viewer.js'):
    latest_frame: bytes | None = None
    frame_id: int = 0
    cond: asyncio.Condition = asyncio.Condition()
    _thread_queue: Queue[bytes] = Queue(maxsize=1)

    def __init__(self, endpoint: str = '/mjpeg', quality: int = 80):
        super().__init__()
        self._props['endpoint'] = endpoint
        self.endpoint = endpoint
        self.quality = quality

        # start up an async task that will read from the thread‐safe queue
        @app.on_startup
        async def _start_queue_reader():
            while True:
                # wait for the next JPEG from your video thread
                data = await asyncio.to_thread(OpencvViewer._thread_queue.get)
                async with OpencvViewer.cond:
                    OpencvViewer.latest_frame = data
                    OpencvViewer.frame_id += 1
                    OpencvViewer.cond.notify_all()

        self._register()

    def stream(self, frame: np.ndarray) -> None:
        """
        Called from your Thread-1.  Just drop into the queues and return immediately.
        """
        success, buf = cv2.imencode('.jpg', frame,
                                    [cv2.IMWRITE_JPEG_QUALITY, self.quality])
        if not success:
            return
        data = buf.tobytes()
        try:
            OpencvViewer._thread_queue.put_nowait(data)
        except Full:
            # if the queue is full, drop the old frame
            _ = OpencvViewer._thread_queue.get_nowait()
            OpencvViewer._thread_queue.put_nowait(data)

    def _register(self):
        @app.get(self.endpoint)
        async def mjpeg_endpoint(request: Request):
            boundary = "--frame"

            async def generator():
                last_id = 0
                while True:
                    if await request.is_disconnected():
                        break

                    # wait for a newer frame
                    async with OpencvViewer.cond:
                        await OpencvViewer.cond.wait_for(lambda: OpencvViewer.frame_id > last_id)
                        last_id = OpencvViewer.frame_id
                        frame = OpencvViewer.latest_frame

                    if not frame:
                        continue

                    yield (
                            boundary.encode() +
                            b"\r\n"
                            b"Content-Type: image/jpeg\r\n"
                            b"Content-Length: " + str(len(frame)).encode() +
                            b"\r\n\r\n" + frame + b"\r\n"
                    )

            return StreamingResponse(generator(), media_type="multipart/x-mixed-replace; boundary=frame")
