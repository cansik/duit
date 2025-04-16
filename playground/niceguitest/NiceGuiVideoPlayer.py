import argparse
import asyncio
import time
from pathlib import Path
from threading import Thread
from typing import Optional

import cv2
import webview
from fastapi import WebSocket
from nicegui import ui, app

from playground.niceguitest.components.video_stream import VideoStream

video_stream: Optional[VideoStream] = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("video")
    return parser.parse_args()


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


def run_nice_gui(web_port: int):
    global video_stream
    video_stream = VideoStream().classes('w-full h-full')
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
