import asyncio
import uuid
from queue import Queue, Full

import numpy as np
from fastapi import Request
from fastapi.responses import StreamingResponse
from nicegui import app
from nicegui.element import Element


class OpencvViewer(Element, component='opencv_viewer.js'):
    """
    NiceGUI component for MJPEG streaming of numpy image arrays.

    :param endpoint: HTTP endpoint for the MJPEG stream (default: random id is generated).
    :param quality: JPEG compression quality (0-100, higher is better quality, default: 80).
    :param frame_queue_size: Maximum number of frames to buffer (default: 1).
    :param block_on_full: If True, block the producer when the queue is full;
                          if False, drop the oldest frame when full (default: False).
    """

    def __init__(
            self,
            endpoint: str | None = None,
            quality: int = 80,
            frame_queue_size: int = 1,
            block_on_full: bool = False,
    ):
        super().__init__()

        # generate a new random endpoint for this component
        if endpoint is None:
            endpoint_id = uuid.uuid4().hex[:5]
            endpoint = f"/stream/{endpoint_id}"

        self._props['endpoint'] = endpoint
        self.endpoint = endpoint
        self.quality = quality
        self.frame_queue_size = frame_queue_size
        self.block_on_full = block_on_full

        # Shared state for latest frame broadcast
        self.latest_frame: bytes | None = None
        self.frame_id: int = 0
        self.cond: asyncio.Condition = asyncio.Condition()

        # Thread-safe queue holding JPEG bytes
        self._thread_queue: Queue[bytes] = Queue(maxsize=self.frame_queue_size)

        # Background task: pull from thread queue, update shared frame, notify viewers
        @app.on_startup
        async def _start_queue_reader():
            while True:
                data = await asyncio.to_thread(self._thread_queue.get)
                async with self.cond:
                    self.latest_frame = data
                    self.frame_id += 1
                    self.cond.notify_all()

        self._register()

    def stream(self, frame: np.ndarray) -> None:
        """
        Push an OpenCV BGR frame into the streaming pipeline.

        :param frame: OpenCV image (BGR numpy array) to encode and enqueue.
        """
        import cv2
        success, buf = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, self.quality])
        if not success:
            return
        data = buf.tobytes()

        if self.block_on_full:
            # Block until there's room in the queue
            self._thread_queue.put(data)
        else:
            # Drop oldest if queue is full
            try:
                self._thread_queue.put_nowait(data)
            except Full:
                _ = self._thread_queue.get_nowait()
                self._thread_queue.put_nowait(data)

    def _register(self) -> None:
        @app.get(self.endpoint)
        async def mjpeg_endpoint(request: Request):
            """
            HTTP endpoint that streams multipart MJPEG to clients.
            """
            boundary = "--frame"

            async def generator():
                """
                Async generator yielding JPEG frames to each connected client.
                """
                last_id = 0
                while True:
                    if await request.is_disconnected():
                        break

                    # wait for a newer frame than we've sent
                    async with self.cond:
                        await self.cond.wait_for(lambda: self.frame_id > last_id)
                        last_id = self.frame_id
                        frame = self.latest_frame

                    if not frame:
                        continue

                    yield (
                            boundary.encode() + b"\r\n"
                                                b"Content-Type: image/jpeg\r\n"
                                                b"Content-Length: " + str(len(frame)).encode() + b"\r\n\r\n"
                            + frame + b"\r\n"
                    )

            return StreamingResponse(
                generator(),
                media_type="multipart/x-mixed-replace; boundary=frame"
            )
