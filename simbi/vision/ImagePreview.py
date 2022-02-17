from abc import ABC, abstractmethod

import numpy as np


class ImagePreview(ABC):

    @abstractmethod
    def __init__(self, title: str = "Image Preview", width: int = 640, height: int = 480):
        self._title = title
        self._width = width
        self._height = height

        self._is_open = False

    @abstractmethod
    def open(self):
        self._is_open = True

    @abstractmethod
    def display(self, image: np.ndarray):
        pass

    @abstractmethod
    def close(self):
        self._is_open = False

    @abstractmethod
    def set_window_size(self, width: int, height: int):
        self._width = width
        self._height = height

