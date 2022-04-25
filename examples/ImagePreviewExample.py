import numpy as np

from duit.vision.Open3dImagePreview import Open3dImagePreview

if __name__ == "__main__":
    preview = Open3dImagePreview("Example")
    preview.open()

    color = 200
    img = np.zeros([100, 100, 3], dtype=np.uint8)

    while True:
        img.fill(color)
        color = (color + 1) % 255

        preview.display(img)

    preview.close()
