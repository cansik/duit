import argparse
from pathlib import Path
from threading import Thread
from typing import Optional

import cv2
import webview
from nicegui import ui

from duit.utils import os_utils
from duit.ui.nicegui.components.opencv_viewer import OpencvViewer
from playground.niceguitest.components.video_stream import VideoStream

video_stream: Optional[VideoStream] = None
opencv_viewer: Optional[OpencvViewer] = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("video")
    return parser.parse_args()


def run_nice_gui(web_port: int):
    global video_stream, opencv_viewer
    # video_stream = VideoStream().classes('w-full h-full')
    opencv_viewer = OpencvViewer().classes('w-full h-full')
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
            if video_stream is not None:
                video_stream.stream(frame)
            if opencv_viewer is not None:
                opencv_viewer.stream(frame)
            # time.sleep(delay)
    finally:
        cap.release()


def main() -> None:
    os_utils.disable_app_nap_on_macos()

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
