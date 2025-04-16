import argparse
import base64
import time
from enum import Enum
from pathlib import Path
from queue import Queue, Empty
from threading import Thread

import cv2
import numpy as np
import webview
from nicegui import ui

frame_queue: Queue[str] = Queue(maxsize=1)


class ImageMimeType(Enum):
    BMP = ('.bmp', 'image/bmp')
    DIB = ('.dib', 'image/bmp')  # Windows bitmap
    JPEG = ('.jpg', 'image/jpeg')
    JPE = ('.jpe', 'image/jpeg')
    JPEG2K = ('.jp2', 'image/jp2')
    PNG = ('.png', 'image/png')
    WEBP = ('.webp', 'image/webp')
    PPM = ('.ppm', 'image/x-portable-pixmap')
    PGM = ('.pgm', 'image/x-portable-graymap')
    PBM = ('.pbm', 'image/x-portable-bitmap')
    SR = ('.sr', 'image/x-rgb')
    RAS = ('.ras', 'image/x-cmu-raster')
    TIFF = ('.tiff', 'image/tiff')

    def __init__(self, ext: str, mime: str):
        self.ext = ext
        self.mime = mime


def convert_to_data_uri(
        frame: np.ndarray,
        img_type: ImageMimeType,
        encode_params: list[int] = None
) -> str:
    """
    Converts an OpenCV frame to a Base64-encoded data URI using the specified image type.

    Args:
        frame:        The image as a NumPy array (BGR).
        img_type:     One of ImageMimeType enum members.
        encode_params:
                      Optional OpenCV encoding parameters
                      (e.g. [cv2.IMWRITE_JPEG_QUALITY, 90]).

    Returns:
        A string of the form "data:<mime>;base64,<base64-data>".

    Raises:
        ValueError: If encoding fails.
    """
    success, buf = cv2.imencode(img_type.ext, frame, encode_params or [])
    if not success:
        raise ValueError(f"Could not encode frame to format {img_type.ext}")

    b64 = base64.b64encode(buf).decode('ascii')
    return f'data:{img_type.mime};base64,{b64}'


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("video")
    return parser.parse_args()


def run_nice_gui(web_port: int):
    video_image = ui.interactive_image().classes('w-full h-full')

    def update_frame():
        try:
            data_uri = frame_queue.get_nowait()
            # thread‐safe: only the main GUI thread touches the widget here
            video_image.set_source(data_uri)
            video_image.update()
        except Empty:
            pass

    ui.timer(1 / 30, update_frame)
    ui.run(reload=False, port=web_port, dark=True, show=False)


def run_video_thread(video_path: Path):
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open video {video_path}")
    # compute per‐frame delay
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    delay = 1.0 / fps

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_MSEC, 0.0)
                continue
            # convert and enqueue, dropping old if needed
            start = time.perf_counter()
            data_uri = convert_to_data_uri(frame, ImageMimeType.JPEG, [cv2.IMWRITE_JPEG_QUALITY, 70])
            end = time.perf_counter()
            print(f"Encoding time: {end - start:.3f}s")
            try:
                frame_queue.put(data_uri, block=False)
            except:
                # queue full → remove old and retry
                try:
                    frame_queue.get(block=False)
                    frame_queue.put(data_uri, block=False)
                except:
                    pass
            time.sleep(delay)
    finally:
        cap.release()


def main() -> None:
    args = parse_args()
    video_path = Path(args.video)

    web_port = 8422

    Thread(target=run_video_thread, args=(video_path,), daemon=True).start()
    Thread(target=run_nice_gui, args=(web_port,), daemon=True).start()

    webview.create_window("NiceGUI Video Player", f"http://localhost:{web_port}")
    webview.start()

    exit(0)


if __name__ == "__main__":
    main()
