from functools import partial

import cv2
import numpy as np
from open3d.cpu.pybind.geometry import Image
from open3d.cpu.pybind.visualization import gui

app = gui.Application.instance
app.initialize()

window: gui.Window = gui.Application.instance.create_window("Demo Window", 200, 400)
vert = gui.ScrollableVert()

for i in range(10):
    image_widget = gui.ImageWidget()
    image = np.zeros((100, 400, 3), dtype=np.uint8)

    cv2.line(image, (0, 100 - 1), (400 - 1, 100 - 1), (255, 255, 255), 2)

    cv2.putText(
        img=image,
        text=f"Image {i}",
        org=(0, 50),
        fontFace=cv2.FONT_HERSHEY_DUPLEX,
        fontScale=2.0,
        color=(255, 255, 255),
        thickness=3
    )


    def mouse_event(id: int, e: gui.MouseEvent) -> gui.Widget.EventCallbackResult:
        if e.type == gui.MouseEvent.BUTTON_DOWN:
            print(f"clicked on {id}")
        return gui.Widget.EventCallbackResult.IGNORED


    image_widget.update_image(Image(image))
    image_widget.set_on_mouse(partial(mouse_event, i))
    vert.add_child(image_widget)

window.add_child(vert)

app.run()
