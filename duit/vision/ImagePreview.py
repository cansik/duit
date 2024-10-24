from abc import ABC, abstractmethod

import numpy as np


class ImagePreview(ABC):
    """
    Abstract base class for image preview interfaces.

    Args:
        None
    """

    @abstractmethod
    def __init__(self, title: str = "Image Preview", width: int = 640, height: int = 480):
        """
        Initialize the ImagePreview instance.

        Args:
            title (str): The title of the image preview window.
            width (int): The width of the image preview window.
            height (int): The height of the image preview window.
        """
        self._title = title
        self._width = width
        self._height = height
        self._is_open = False

    @abstractmethod
    def open(self):
        """
        Open the image preview window.

        Args:
            None
        """
        self._is_open = True

    @abstractmethod
    def display(self, image: np.ndarray):
        """
        Display an image in the preview window.

        Args:
            image (np.ndarray): The image to be displayed in the preview window.
        """
        pass

    @abstractmethod
    def close(self):
        """
        Close the image preview window.

        Args:
            None
        """
        self._is_open = False

    @abstractmethod
    def set_window_size(self, width: int, height: int):
        """
        Set the size of the image preview window.

        Args:
            width (int): The new width of the window.
            height (int): The new height of the window.
        """
        self._width = width
        self._height = height
